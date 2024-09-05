
"""

La gestion de Usuario, crear modificar eliminar adminsitar va pasar al archivo userController.py
ubicado en apps/usuarios/controller

"""


from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from apps.api.skilling.models import Cuenta
from ....usuarios.models import Usuario
from apps.api.skilling.models import Afiliado
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
import json 
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model



###########################################################################################################################
############################### Leer comentario de arriba #################################################################
###########################################################################################################################
                                                  ##
                                                ######
                                              ##########
                                            ##############
                                                #####
                                                #####
                                                #####
                                                #####
                                                #####
                                                
@csrf_exempt
def postNewAfiliado(request):
    if request.method == 'POST':
        # if 'application/json' in request.content_type:
            try:
                afiliados = Afiliado.objects.all()
                
                # Decodificar el cuerpo de la solicitud como JSON
                fpa = request.POST.get('fpa').upper()
                url = request.POST.get('url')
                upline = request.POST.get('up_line').upper()

                cuenta = Cuenta.objects.filter(fpa=fpa)
                if not cuenta.exists():
                    c = Cuenta(fpa=fpa)
                    c.save()
                # Crear un nuevo usuario y guardar los datos en la base de datos
                new_afiliado = Afiliado(
                    fpa = fpa,
                    url=url,
                    upline=upline,
                )
                print(new_afiliado.fpa)
                if afiliados.exists():
                    for a in afiliados:
                        if not (a.fpa==fpa and a.url==url and a.upline == upline):
                            new_afiliado.save()
                else:
                    new_afiliado.save()
                return JsonResponse({'message': 'Datos recibidos y guardados con éxito'},status=200)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Error al decodificar el JSON'}, status=402)
        # else:
        #     return JsonResponse({'error': 'Tipo de contenido no válido'}, status=406)
    else:
        return JsonResponse({'error': 'Método HTTP no válido'}, status=405)


@csrf_exempt
def postNewUser(request):
    if request.method == 'POST':
        if 'application/json' in request.content_type:
            try:
                # Decodificar el cuerpo de la solicitud como JSON
                data = json.loads(request.body)
                usuario = Usuario.objects.all()
                
                # Buscar el afiliado con el FPA proporcionado
                afiliados = Afiliado.objects.filter(fpa=data.get('fpa'))
                
                if afiliados.exists():
                    uplink = afiliados[0].upline
                    link = afiliados[0].url 

                    # Crear un nuevo usuario y preparar los datos
                    new_user = Usuario(
                        username=(data.get('fpa') + "_" + data.get('first_name')).replace(' ', '_'),
                        fpa=data.get('fpa'),
                        email=data.get('email'),
                        first_name=data.get('first_name'),
                        last_name=data.get('last_name'),
                        telephone=data.get('telephone'),
                        wallet=data.get('wallet'),
                        uplink=uplink or '',
                        link=link or ''
                    )

                    # Hashear la contraseña antes de guardarla
                    new_user.set_password(data.get('password'))

                    new_user.registrado = True

                    # Verificar si el usuario ya está registrado por FPA
                    if not usuario.filter(fpa=data.get('fpa')).exists():
                        new_user.save()  # Guardar el usuario en la base de datos
                        return JsonResponse({'message': 'Datos recibidos y guardados con éxito'}, status=200)
                    else:
                        return JsonResponse({'message': 'Usuario ya registrado'}, status=401)
                else:
                    return JsonResponse({'message': 'Usuario no habilitado para registrarse'}, status=402)

            except json.JSONDecodeError:
                return JsonResponse({'message': 'Error al decodificar el JSON'}, status=403)
        else:
            return JsonResponse({'message': 'Tipo de contenido no válido'}, status=404)
    else:
        return JsonResponse({'message': 'Método HTTP no válido'}, status=405)



# def login(request, email):
#     if request.method == 'GET':
#         try:
#             usuario = get_object_or_404(Usuario, email__iexact=email)
            
#             # Crear una lista de roles con atributos serializables
#             roles = []
#             for rol in usuario.roles.all():
#                 roles.append({
#                     'id': rol.rol_id,
#                     'rol': rol.rol.name,  # Asegúrate de que 'rol' sea un atributo serializable, no un objeto.
#                     'fecha_asignacion': rol.fecha_asignacion.isoformat()  # Serializar la fecha en formato ISO 8601
#                 })
                
#             servicios = []
            
#             for servicio in usuario.serviciosUsuario.all():
#                 servicios.append({
#                     'id': servicio.servicio_id,
#                     'servicio': servicio.servicio.name
#                 })
            
#             urls = []
            
#             for url in usuario.urls.all():
#                 urls.append({
#                     'id': url.url_id,
#                     'url': url.url
#                 })

#             data = {
#                 'fpa': usuario.fpa,
#                 'email': usuario.email,
#                 'first_name': usuario.first_name,
#                 'password': usuario.password,  # Considera no enviar la contraseña por razones de seguridad
#                 'telephone': usuario.telephone,
#                 'wallet': usuario.wallet,
#                 'uplink': usuario.uplink,
#                 'link': usuario.link,
#                 'roles': roles,  # Convertir la relación a lista de roles
#                 'servicios': servicios,
#                 'registrado': usuario.registrado,
#                 'status': usuario.aceptado,
#                 'idCliente': usuario.idCliente,
#                 'aceptado': usuario.aceptado,
#                 'fondeado': usuario.fondeado,
#                 'eliminado': usuario.eliminado,
#                 'userTelegram': usuario.userTelegram,
#                 'urls': urls
#             }

#             return JsonResponse({'data': data})
#         except Usuario.DoesNotExist:
#             return JsonResponse({'message': 'Usuario no encontrado'}, status=404)
#     else:
#         return JsonResponse({'message': 'Método HTTP no válido'}, status=405)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        email = body_data.get('email')
        password = body_data.get('password')

        try:
            # Obtener el usuario basado en el email
            usuario = Usuario.objects.get(email=email)

            # Verificar si la contraseña es correcta usando check_password
            if check_password(password, usuario.password):
                # Generar los tokens JWT
                refresh = RefreshToken.for_user(usuario)

                # Crear una lista de roles con atributos serializables
                roles = []
                for rol in usuario.roles.all():
                    roles.append({
                        'id': rol.rol_id,
                        'rol': rol.rol.name,
                        'fecha_asignacion': rol.fecha_asignacion.isoformat()
                    })
                
                servicios = []
                for servicio in usuario.serviciosUsuario.all():
                    servicios.append({
                        'id': servicio.servicio_id,
                        'servicio': servicio.servicio.name
                    })

                urls = []
                for url in usuario.urls.all():
                    urls.append({
                        'id': url.id,
                        'url': url.url
                    })

                data = {
                    'fpa': usuario.fpa,
                    'email': usuario.email,
                    'first_name': usuario.first_name,
                    'telephone': usuario.telephone,
                    'wallet': usuario.wallet,
                    'uplink': usuario.uplink,
                    'link': usuario.link,
                    'roles': roles,
                    'servicios': servicios,
                    'registrado': usuario.registrado,
                    'status': usuario.aceptado,
                    'idCliente': usuario.idCliente,
                    'aceptado': usuario.aceptado,
                    'fondeado': usuario.fondeado,
                    'eliminado': usuario.eliminado,
                    'userTelegram': usuario.userTelegram,
                    'urls': urls,
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                }

                return JsonResponse({'data': data}, status=200)
            else:
                return JsonResponse({'message': 'Credenciales inválidas'}, status=401)
        except Usuario.DoesNotExist:
            return JsonResponse({'message': 'Usuario no encontrado'}, status=404)
    else:
        return JsonResponse({'message': 'Método HTTP no válido'}, status=405)




@csrf_exempt
def getUserById(request, pk):
    
    if request.method == 'GET':
        try:
            usuario = Usuario.objects.get(fpa=pk)  # Corrige el nombre del campo fpa
            data = {
                'fpa': usuario.fpa,
                'email': usuario.email,
                'first_name': usuario.first_name,
                'password': usuario.password,
                'telephone': usuario.telephone,
                'wallet': usuario.wallet,
                'uplink': usuario.uplink,
                'link': usuario.link,
                'roles': usuario.roles,
                'registrado':usuario.registrado,
                'status': usuario.aceptado,
            }
            return JsonResponse({'data': data})
        except Usuario.DoesNotExist:
            return JsonResponse({'message': 'Usuario no encontrado'}, status=404)
    else:
        return JsonResponse({'message':'Metodo invalido'})

@csrf_exempt
def updateUserById(request, pk):
    try:
        if request.method == 'POST' or request.method == 'PUT':
            
            try:
                body_data = json.loads(request.body)  # Decodifica el cuerpo como JSON
            except json.JSONDecodeError:
                # Si hay un error al decodificar JSON, devuelve una respuesta de error
                return JsonResponse({'message': 'Datos inválidos en el cuerpo (body)'}, status=400)
            
            # Aquí puedes acceder a los datos enviados en el cuerpo (body)
            name = body_data.get('name')
            email = body_data.get('email')
            roles = body_data.get('roles')
            status = body_data.get('status')

            print(status)
            # Luego, puedes usar los datos para actualizar el objeto Usuario
            usuario = Usuario.objects.get(fpa=pk)
            usuario.first_name = name
            usuario.email = email
            usuario.roles = roles
            usuario.aceptado= status
            usuario.save()

        # Si todo salió bien, devuelve los datos actualizados como respuesta
        data = {
                'fpa': usuario.fpa,
                'email': usuario.email,
                'first_name': usuario.first_name,
                'password': usuario.password,
                'telephone': usuario.telephone,
                'wallet': usuario.wallet,
                'uplink': usuario.uplink,
                'link': usuario.link,
                'roles': usuario.roles,
                'registrado':usuario.registrado,
                'status': usuario.aceptado,
            }
        
        return JsonResponse({'data': data})
    except Usuario.DoesNotExist:
        return JsonResponse({'message': 'Usuario no encontrado'}, status=404)

@csrf_exempt
def updatePerfilUser(request, pk):
    
    if request.method == 'POST' or request.method == 'PUT':
        try:
            try:
                body_data = json.loads(request.body)  # Decodifica el cuerpo como JSON
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Datos inválidos en el cuerpo (body)'}, status=400)
            
            users = Usuario.objects.get(fpa=pk)
            users.telephone=body_data.get('telephone')
            users.wallet=body_data.get('wallet')
            users.email=body_data.get('email')
            users.link=body_data.get('link')
            
            users.save()
            
            data = {
                'fpa': users.fpa,
                'email': users.email,
                'first_name': users.first_name,
                'password': users.password,
                'telephone': users.telephone,
                'wallet': users.wallet,
                'uplink': users.uplink,
                'link': users.link,
                'roles': users.roles,
                'registrado':users.registrado,
                'status': users.aceptado,
            }
            
            return JsonResponse({'data':data})
        except Exception as e:
            return JsonResponse({'Error':e})
    else:
        return JsonResponse({'Error':'Metodo Invalido'})

@csrf_exempt   
def users(request):
    
    if request.method == 'GET':
        try:
            usuarios = Usuario.objects.all()
            data = []
            for u in usuarios:
                if u.eliminado is False:
                    data.append({
                        'fpa':u.fpa,
                        'email':     u.email,
                        'first_name':u.first_name,
                        'password':  u.password,
                        'telephone': u.telephone,
                        'wallet':    u.wallet,
                        'uplink':    u.uplink,
                        'link':      u.link,
                        'roles':     u.roles,
                        'registrado':u.registrado,
                        'status':    u.aceptado,
                    })
            response =  JsonResponse({'data': data})
            return response

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error al decodificar el JSON'}, status=400)
    else:
        return JsonResponse({'Error':'metodo invalido'})

@csrf_exempt  
def usuarioValido(request,email,password):
    
    users = Usuario.objects.all()
    data= False
    for user in users:
        if user.email == email and user.password == password:
            data= True
        
    
    response = JsonResponse({'data': data})
    # response['Access-Control-Allow-Origin'] = '*' 
    
    return response

@csrf_exempt    
def eliminarUser(request,pk):

    if request.method == 'DELETE':
        
        user = Usuario.objects.get(fpa=pk)
        user.eliminado = True
        user.save()
            
        response = JsonResponse({'data': 'User eliminado'})
    else:
        response = JsonResponse({'Error':'Metodo invalido'})

    return response


@csrf_exempt   
def users_pendientes(request):
    try:
        usuarios = Usuario.objects.all()
        data = []
        for u in usuarios:
            if u.aceptado is False and u.eliminado is False:
                data.append({
                    'fpa':u.fpa,
                    'email':     u.email,
                    'first_name':u.first_name,
                    'password':  u.password,
                    'telephone': u.telephone,
                    'wallet':    u.wallet,
                    'uplink':    u.uplink,
                    'link':      u.link,
                    'roles':     u.roles,
                    'registrado':u.registrado,
                    'status':    u.aceptado,
                })
        response =  JsonResponse({'data': data})
        return response

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Error al decodificar el JSON'}, status=400)
    

@csrf_exempt   
def users_eliminados(request):
    try:
        usuarios = Usuario.objects.all()
        data = []
        for u in usuarios:
            if u.eliminado is True:
                data.append({
                    'fpa':u.fpa,
                    'email':     u.email,
                    'first_name':u.first_name,
                    'password':  u.password,
                    'telephone': u.telephone,
                    'wallet':    u.wallet,
                    'uplink':    u.uplink,
                    'link':      u.link,
                    'roles':     u.roles,
                    'registrado':u.registrado,
                    'status':    u.aceptado,
                })
        response =  JsonResponse({'data': data})
        return response

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Error al decodificar el JSON'}, status=400)

@csrf_exempt  
def updatePassword(request, pk):
    if request.method == 'PUT':
        try:
            body = json.loads(request.body)
            usuario = Usuario.objects.get(fpa=pk)

            # Obtener la nueva contraseña del cuerpo de la solicitud
            new_password = body.get('password')

            if new_password:
                # Hashear la contraseña usando set_password
                usuario.set_password(new_password)

                # Guardar los cambios
                usuario.save()

                return JsonResponse({'data': 'Contraseña modificada con éxito'}, status=200)
            else:
                return JsonResponse({'Error': 'Contraseña no proporcionada'}, status=400)
        
        except Usuario.DoesNotExist:
            return JsonResponse({'Error': 'Usuario no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'Error': str(e)}, status=500)
    
    else:
        return JsonResponse({'Error': 'Método HTTP incorrecto'}, status=405)



@csrf_exempt  
def deleteUser(request,pk):
    try:
        if request.method == 'POST':
            user = Usuario.objects.get(fpa=pk)
            user.delete()
            return JsonResponse({'data':'Usuario eliminado'})
        else:
            return JsonResponse({'Error':'Metodo invalido'})
    except Exception as e:
        print(e.__str__())
        return JsonResponse({'Error':e})