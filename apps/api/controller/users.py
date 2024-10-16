from django.http import JsonResponse
from django.shortcuts import render
from ...usuarios.models import Usuario,Cuenta
from ...afiliado.models import Afiliado, Cliente
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
import json 


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
            
                afiliados = Afiliado.objects.filter(fpa=data.get('fpa'))
                
                if afiliados.exists():
                    print(afiliados[0].fpa)
                    uplink = afiliados[0].upline
                    link=afiliados[0].url 
                # Crear un nuevo usuario y guardar los datos en la base de datos
                
                    new_user = Usuario(
                        username = (data.get('fpa') + "_" + data.get('first_name')).replace(' ', '_'),
                        fpa=data.get('fpa'),
                        email=data.get('email'),
                        first_name=data.get('first_name'),
                        last_name=data.get('last_name'),
                        password=data.get('password'),
                        telephone=data.get('telephone'),
                        wallet=data.get('wallet'),
                        uplink=uplink or '',
                        link=link or ''
                    )
                    new_user.registrado = True
                    if not usuario.filter(fpa=data.get('fpa')).exists():
                        new_user.save()
                    else:
                        return JsonResponse({'message':'Usuario ya registrado'},status=401)
                else:
                    return JsonResponse({'message':'Usuario no Habilidato para registrarse'},status=402)
                
                return JsonResponse({'message': 'Datos recibidos y guardados con éxito'},status=200)
            
            except json.JSONDecodeError:
                return JsonResponse({'message': 'Error al decodificar el JSON'}, status=403)
            
        else:
            return JsonResponse({'message': 'Tipo de contenido no válido'}, status=404)
        
    else:
        return JsonResponse({'message': 'Método HTTP no válido'}, status=405)

@csrf_exempt
def getUser(request,email):
    if request.method == 'GET':
        # Asegúrate de que la solicitud tenga el tipo de contenido adecuado (application/json)
            try:
                usuarios = Usuario.objects.all()
                data = []
                for u in usuarios:
                    
                    if u.email.upper() == email.upper():
                
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
                            'status':    u.aceptado
                        })

                return JsonResponse({'data': data})
            except json.JSONDecodeError:
                return JsonResponse({'message': 'Error al decodificar el JSON'}, status=400)
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
def updatePassword(request,pk):
    if request.method == 'PUT':
        try:
            body = json.loads(request.body)
            usuario = Usuario.objects.get(fpa=pk)
            
            usuario.password= body.get('password')
            
            usuario.save()
            
            return JsonResponse({'data':'password modificado con exito'})
            
        except Exception as e:
            return JsonResponse({'Error':e})
    
    else:
        return JsonResponse({'Error':'Metodo incorrecto'})



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
    



@csrf_exempt  
def getUserNewFormat(request):
    if request.method == 'GET':
        try:
            # Obtener todos los usuarios y clientes
            usuarios = Usuario.objects.all()
            clientes = Cliente.objects.all()

            data = []

            # Combinar los usuarios
            for usuario in usuarios:
                combined_data = {
                    'fpa': usuario.fpa,
                    'nombre': usuario.first_name,
                    'apellido': usuario.last_name,
                    'email': usuario.email,
                    'telefono': usuario.telephone,
                    'wallet': usuario.wallet,
                    'uplink': usuario.uplink,
                    'link': usuario.link,
                    'roles': [3],
                    'registrado': usuario.registrado,
                    'status': usuario.aceptado,
                    'idCliente': None,
                    'userTelegram': None,
                    'password': usuario.password
                }
                data.append(combined_data)

            # Combinar los clientes
            for cliente in clientes:
                combined_data = {
                    'fpa': None,  # Cliente no tiene campo fpa
                    'nombre': cliente.nombre,
                    'apellido': cliente.apellido,
                    'email': cliente.correo,
                    'telefono': cliente.telefono,
                    'wallet': None,  # Cliente no tiene campo wallet
                    'uplink': cliente.idAfiliado,  # Cliente no tiene campo uplink
                    'link': None,    # Cliente no tiene campo link
                    'roles': [2],   # Cliente no tiene campo roles
                    'registrado': None,  # Cliente no tiene campo registrado
                    'status': None,  # Cliente no tiene campo aceptado
                    'idCliente': cliente.idCliente,
                    'userTelegram': cliente.userTelegram,
                    'password': cliente.idCliente
                }
                data.append(combined_data)

            # Devolver el array combinado
            return JsonResponse({'data': data}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    else:
        return JsonResponse({'error': 'Método HTTP no válido'}, status=405)

# @csrf_exempt
# def getUserNewFormat(request):
#     if request.method == 'GET':
#         try:
#             # Obtener todos los usuarios
#             usuarios = Usuario.objects.all()
#             clientes = Cliente.objects.all()
#             data = []
            
#             for usuario in usuarios:
#                 # Crear el objeto combinado
#                 combined_data = {
#                     'fpa': usuario.fpa,
#                     'nombre': usuario.first_name ,
#                     'apellido': usuario.last_name ,
#                     'email': usuario.email ,
#                     'telefono': usuario.telephone ,
#                     'wallet': usuario.wallet ,
#                     'uplink': usuario.uplink ,
#                     'link': usuario.link ,
#                     'roles': usuario.roles ,
#                     'registrado': usuario.registrado,
#                     'status': usuario.aceptado,
#                     'idCliente': None ,
#                     'UserTelegram': None ,
#                 }
                
#                 data.append(combined_data)
            
#             return JsonResponse({'data': data}, status=200)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)
#     else:
#         return JsonResponse({'error': 'Método HTTP no válido'}, status=405)
