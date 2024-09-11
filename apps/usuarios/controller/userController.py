import json
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
import requests
from apps.api.skilling.models import Afiliado, Cuenta
from apps.usuarios.models import (
    Rol,
    Servicio,
    Usuario,
    UsuarioRol,
    UsuarioServicio,
    Url
)
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password


from rest_framework.exceptions import AuthenticationFailed


@csrf_exempt
def login(request):
    print("login request", request.method, request.body)
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        email = body_data.get('email')
        password = body_data.get('password')
        urls = Url.objects.all()

        try:
            print("checking user")
            # Obtener el usuario basado en el email
            usuario = Usuario.objects.get(email=email)
            print("user found", usuario)

            # Verificar si la contraseña es correcta usando check_password
            if check_password(password, usuario.password):
                print("password correct")
                # Generar los tokens JWT
                refresh = RefreshToken.for_user(usuario)
                print("refresh token generated", refresh)

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
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'url_livecommunity':f'{urls[0].url}{usuario.fpa}' if usuario.fpa != None  else '',
                    'url_skilling':f'{urls[1].url}{usuario.fpa}' if usuario.fpa != None  else '',
                }

                return JsonResponse({'data': data}, status=200)
            else:
                print("wrong password")
                return JsonResponse({'message': 'Credenciales inválidas'}, status=401)
        except Usuario.DoesNotExist:
            print("user not found")
            return JsonResponse({'message': 'Usuario no encontrado'}, status=404)
    else:
        print("wrong method")
        return JsonResponse({'message': 'Método HTTP no válido'}, status=405)




@csrf_exempt
def postNewUsers(request):
    try:
        # Hacer la petición a la URL externa para obtener los datos
        response = requests.get("https://livecommunity.info/api/userNewFormat/")

        # Verificar si la petición fue exitosa (status code 200)
        if response.status_code == 200:
            # Decodificar la respuesta JSON
            external_data = response.json()

            # Obtener la lista de usuarios desde la respuesta externa
            usuarios = external_data.get("data", [])

            for user_data in usuarios:
                # Generar el username a partir del apellido y nombre
                base_username = (user_data.get("apellido") + "_" + user_data.get("nombre")).replace(" ", "_")

                # Verificar si el usuario con ese username ya existe
                existing_user = Usuario.objects.filter(username=base_username).first()

                if existing_user:
                    # El usuario ya existe, actualizar datos si fpa o idCliente son None
                    if not existing_user.fpa and user_data.get("fpa"):
                        existing_user.fpa = user_data.get("fpa")
                    if not existing_user.idCliente and user_data.get("idCliente"):
                        existing_user.idCliente = user_data.get("idCliente")
                    existing_user.email = user_data.get("email")  # Actualiza el correo también
                    existing_user.telephone = user_data.get("telefono")
                    existing_user.wallet = user_data.get("wallet")
                    existing_user.uplink = user_data.get("uplink") or existing_user.uplink
                    existing_user.link = user_data.get("link") or existing_user.link
                    existing_user.registrado = user_data.get("registrado", False) if user_data.get("registrado") is not None else False
                    existing_user.aceptado = user_data.get("status", False) if user_data.get("status") is not None else False
                    existing_user.userTelegram = user_data.get("userTelegram") or existing_user.userTelegram

                    # Guardar cambios del usuario existente
                    existing_user.save()

                    # Verificar si los roles que trae el dato ya están asignados
                    roles = user_data.get("roles", [])  # Lista de IDs de roles
                    for rol_id in roles:
                        try:
                            rol = Rol.objects.get(id=rol_id)
                            if not UsuarioRol.objects.filter(usuario=existing_user, rol=rol).exists():
                                UsuarioRol.objects.create(usuario=existing_user, rol=rol)
                        except Rol.DoesNotExist:
                            return JsonResponse(
                                {"message": f"Rol con ID {rol_id} no existe"}, status=400
                            )

                    # Verificar si los servicios ya están asignados
                    servicios = user_data.get("servicios", [1])  # Lista de IDs de servicios
                    for servicio_id in servicios:
                        try:
                            servicio = Servicio.objects.get(id=servicio_id)
                            if not UsuarioServicio.objects.filter(usuario=existing_user, servicio=servicio).exists():
                                UsuarioServicio.objects.create(usuario=existing_user, servicio=servicio)
                        except Servicio.DoesNotExist:
                            return JsonResponse(
                                {"message": f"Servicio con ID {servicio_id} no existe"}, status=400
                            )

                else:
                    # Crear nuevo usuario si no existe
                    new_user = Usuario(
                        username=base_username,
                        fpa=user_data.get("fpa") or None,
                        idCliente=user_data.get("idCliente") or None,
                        email=user_data.get("email"),
                        first_name=user_data.get("nombre"),
                        last_name=user_data.get("apellido"),
                        telephone=user_data.get("telefono"),
                        wallet=user_data.get("wallet"),
                        uplink=user_data.get("uplink") or "",
                        link=user_data.get("link") or "https://livecommunity.info/Afiliado/",
                        registrado=user_data.get("registrado", False) if user_data.get("registrado") is not None else False,
                        aceptado=user_data.get("status", False) if user_data.get("status") is not None else False,
                        userTelegram=user_data.get("userTelegram") or None,
                        password=user_data.get("password", "default_password"),
                    )

                    try:
                        # Guardar el nuevo usuario en la base de datos
                        new_user.save()

                        # Asignar roles al nuevo usuario
                        roles = user_data.get("roles", [])  # Lista de IDs de roles
                        for rol_id in roles:
                            try:
                                rol = Rol.objects.get(id=rol_id)
                                UsuarioRol.objects.create(usuario=new_user, rol=rol)
                            except Rol.DoesNotExist:
                                return JsonResponse(
                                    {"message": f"Rol con ID {rol_id} no existe"}, status=400
                                )

                        # Asignar servicios al nuevo usuario (si existen en los datos)
                        servicios = user_data.get("servicios", [])  # Lista de IDs de servicios
                        for servicio_id in servicios:
                            try:
                                servicio = Servicio.objects.get(id=servicio_id)
                                UsuarioServicio.objects.create(usuario=new_user, servicio=servicio)
                            except Servicio.DoesNotExist:
                                return JsonResponse(
                                    {"message": f"Servicio con ID {servicio_id} no existe"}, status=400
                                )

                    except Exception as e:
                        print(f"Error guardando el usuario {new_user.username}: {e}")
                        continue  # Saltamos el usuario que genera el error

            return JsonResponse({"message": "Usuarios creados o actualizados exitosamente"}, status=200)

        else:
            return JsonResponse(
                {"message": "Error en la petición a la URL externa"},
                status=response.status_code,
            )

    except requests.exceptions.RequestException as e:
        return JsonResponse({"message": f"Error de conexión: {str(e)}"}, status=500)
    except json.JSONDecodeError:
        return JsonResponse({"message": "Error al decodificar el JSON"}, status=403)

@csrf_exempt
def postNewUser(request):
    if request.method == 'POST':
        if 'application/json' in request.content_type:
            try:
                # Decodificar el cuerpo de la solicitud como JSON
                user_data = json.loads(request.body)

                print("Recibido user_data:", user_data)

                # Generar el username a partir del apellido y nombre
                try:
                    base_username = (user_data.get("last_name") + "_" + user_data.get("first_name")).replace(" ", "_")
                except Exception as e:
                    print(f"Error generando el username: {e}")
                    return JsonResponse({"message": "Error al crear el usuario"}, status=400)

                print("Username base:", base_username)

                # Verificar si el usuario con ese username ya existe
                existing_user = Usuario.objects.filter(username=base_username).first()

                print("Usuario existente:", existing_user)

                if existing_user:
                    # El usuario ya existe, actualizar datos si fpa o idCliente son None
                    if not existing_user.fpa and user_data.get("fpa"):
                        existing_user.fpa = user_data.get("fpa")
                    if not existing_user.idCliente and user_data.get("idCliente"):
                        existing_user.idCliente = user_data.get("idCliente")
                    existing_user.email = user_data.get("email")
                    existing_user.telephone = user_data.get("telefono")
                    existing_user.wallet = user_data.get("wallet")
                    existing_user.uplink = user_data.get("uplink") or existing_user.uplink
                    existing_user.link = user_data.get("link") or existing_user.link
                    existing_user.registrado = user_data.get("registrado", False) if user_data.get("registrado") is not None else False
                    existing_user.aceptado = user_data.get("status", False) if user_data.get("status") is not None else False
                    existing_user.userTelegram = user_data.get("userTelegram") or existing_user.userTelegram

                    # Hashear y actualizar la contraseña si está presente
                    if user_data.get("password"):
                        existing_user.set_password(user_data.get("password"))

                    # Guardar cambios del usuario existente
                    existing_user.save()

                    print("Usuario existente guardado")

                    # Verificar y asignar roles
                    roles = user_data.get("roles", [])
                    for rol_id in roles:
                        try:
                            rol = Rol.objects.get(id=rol_id)
                            if not UsuarioRol.objects.filter(usuario=existing_user, rol=rol).exists():
                                UsuarioRol.objects.create(usuario=existing_user, rol=rol)
                        except Rol.DoesNotExist:
                            return JsonResponse({"message": f"Rol con ID {rol_id} no existe"}, status=400)

                    # Verificar y asignar servicios
                    servicios = user_data.get("servicios", [])
                    for servicio_id in servicios:
                        try:
                            servicio = Servicio.objects.get(id=servicio_id)
                            if not UsuarioServicio.objects.filter(usuario=existing_user, servicio=servicio).exists():
                                UsuarioServicio.objects.create(usuario=existing_user, servicio=servicio)
                        except Servicio.DoesNotExist:
                            return JsonResponse({"message": f"Servicio con ID {servicio_id} no existe"}, status=400)

                else:
                    # Crear un nuevo usuario si no existe
                    new_user = Usuario(
                        username=base_username,
                        fpa=user_data.get("fpa") or None,
                        idCliente=user_data.get("idCliente") or None,
                        email=user_data.get("email"),
                        first_name=user_data.get("first_name"),
                        last_name=user_data.get("last_name"),
                        telephone=user_data.get("telefono"),
                        wallet=user_data.get("wallet"),
                        uplink=user_data.get("uplink") or "",
                        link=user_data.get("link") or "https://livecommunity.info/Afiliado/",
                        registrado=user_data.get("registrado", False) if user_data.get("registrado") is not None else False,
                        aceptado=user_data.get("status", False) if user_data.get("status") is not None else False,
                        userTelegram=user_data.get("userTelegram") or None,
                    )

                    print("Usuario nuevo:", new_user)

                    # Hashear y establecer la contraseña del nuevo usuario
                    if user_data.get("password"):
                        new_user.set_password(user_data.get("password"))
                    else:
                        # Opción para manejar una contraseña por defecto si no se proporciona una
                        new_user.set_password("default_password")

                    try:
                        # Guardar el nuevo usuario en la base de datos
                        new_user.save()
                        # Asignar roles al nuevo usuario
                        roles = user_data.get("roles", [])
                        for rol_id in roles:
                            try:
                                rol = Rol.objects.get(id=rol_id)
                                UsuarioRol.objects.create(usuario=new_user, rol=rol)
                            except Rol.DoesNotExist:
                                return JsonResponse({"message": f"Rol con ID {rol_id} no existe"}, status=400)

                        # Asignar servicios al nuevo usuario
                        servicios = user_data.get("servicios", [])
                        for servicio_id in servicios:
                            try:
                                servicio = Servicio.objects.get(id=servicio_id)
                                UsuarioServicio.objects.create(usuario=new_user, servicio=servicio)
                            except Servicio.DoesNotExist:
                                return JsonResponse({"message": f"Servicio con ID {servicio_id} no existe"}, status=400)

                    except Exception as e:
                        print(f"Error guardando el usuario {new_user.username}: {e}")
                        return JsonResponse({"message": f"Error guardando el usuario: {e}"}, status=500)

                return JsonResponse({"message": "Usuario creado o actualizado exitosamente"}, status=200)

            except json.JSONDecodeError:
                return JsonResponse({"message": "Error al decodificar el JSON"}, status=403)
        else:
            return JsonResponse({"message": "Tipo de contenido no válido"}, status=404)
    else:
        return JsonResponse({"message": "Método HTTP no válido"}, status=405)
    
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




###########################################################################################################################################################
###########################################################################################################################################################
############################### Este codigo hay que chequearlo y corregirlo################################################################################
###########################################################################################################################################################



@csrf_exempt
def getUserById(request, pk):
    if request.method == 'GET':
        # Autenticación JWT
        jwt_authenticator = JWTAuthentication()
        try:
            # Verifica el JWT en la solicitud
            user, token = jwt_authenticator.authenticate(request)
        except AuthenticationFailed:
            return JsonResponse({'message': 'Token inválido o faltante'}, status=401)

        try:
            # Buscamos al usuario por el campo fpa
            usuario = Usuario.objects.get(fpa=pk)
            urls = Url.objects.all()

            # Creamos la lista de roles serializable
            roles = []
            for rol in usuario.roles.all():
                roles.append({
                    'id': rol.rol_id,
                    'rol': rol.rol.name,
                    'fecha_asignacion': rol.fecha_asignacion.isoformat()
                })

            # Creamos la lista de servicios serializable
            servicios = []
            for servicio in usuario.serviciosUsuario.all():
                servicios.append({
                    'id': servicio.servicio_id,
                    'servicio': servicio.servicio.name
                })

            # Creamos el diccionario de datos del usuario
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
                'url_livecommunity': f'{urls[0].url}{usuario.fpa}' if usuario.fpa is not None else '',
                'url_skilling': f'{urls[1].url}{usuario.fpa}' if usuario.fpa is not None else '',
            }

            # Devolvemos la respuesta en formato JSON
            return JsonResponse({'data': data}, status=200)

        except Usuario.DoesNotExist:
            return JsonResponse({'message': 'Usuario no encontrado'}, status=404)
    else:
        return JsonResponse({'message': 'Método HTTP no válido'}, status=405)



def users(request):
    if request.method == 'GET':
        try:
            # Prefetch para evitar consultas adicionales
            usuarios = Usuario.objects.filter(eliminado=False).prefetch_related('roles__rol', 'serviciosUsuario')
            # Solo obtener las URLs necesarias, si son las primeras dos
            urls = Url.objects.all()[:2]
            
            url_livecommunity_base = urls[0].url if len(urls) > 0 else ''
            url_skilling_base = urls[1].url if len(urls) > 1 else ''
            
            # List comprehension para generar la respuesta
            data = [
                {
                    'fpa': usuario.fpa,
                    'email': usuario.email,
                    'first_name': usuario.first_name,
                    'telephone': usuario.telephone,
                    'wallet': usuario.wallet,
                    'uplink': usuario.uplink,
                    'link': usuario.link,
                    'roles': [{'id': rol.rol_id, 'rol': rol.rol.name} for rol in usuario.roles.all()],  # Cambiamos a rol.rol.name
                    'servicios': [{'id': servicio.servicio_id, 'servicio': servicio.servicio.name} for servicio in usuario.serviciosUsuario.all()],
                    'registrado': usuario.registrado,
                    'status': usuario.aceptado,
                    'idCliente': usuario.idCliente,
                    'aceptado': usuario.aceptado,
                    'fondeado': usuario.fondeado,
                    'eliminado': usuario.eliminado,
                    'userTelegram': usuario.userTelegram,
                    'url_livecommunity': f'{url_livecommunity_base}{usuario.fpa}' if usuario.fpa else '',
                    'url_skilling': f'{url_skilling_base}{usuario.fpa}' if usuario.fpa else '',
                }
                for usuario in usuarios
            ]

            return JsonResponse({'data': data}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error al decodificar el JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método HTTP no válido'}, status=405)

@csrf_exempt   
def users_pendientes(request):
    if request.method == 'GET':
        try:
            # Filtrar usuarios que no están aceptados y no están eliminados
            usuarios = Usuario.objects.filter(aceptado=False, eliminado=False).prefetch_related('roles__rol', 'serviciosUsuario')
            # Obtener las primeras dos URLs, si existen
            urls = Url.objects.all()[:2]
            
            url_livecommunity_base = urls[0].url if len(urls) > 0 else ''
            url_skilling_base = urls[1].url if len(urls) > 1 else ''
            
            # List comprehension para generar la respuesta
            data = [
                {
                    'fpa': usuario.fpa,
                    'email': usuario.email,
                    'first_name': usuario.first_name,
                    'telephone': usuario.telephone,
                    'wallet': usuario.wallet,
                    'uplink': usuario.uplink,
                    'link': usuario.link,
                    'roles': [{'id': rol.rol_id, 'rol': rol.rol.name} for rol in usuario.roles.all()],  # Cambiamos a rol.rol.name
                    'servicios': [{'id': servicio.servicio_id, 'servicio': servicio.servicio.name} for servicio in usuario.serviciosUsuario.all()],
                    'registrado': usuario.registrado,
                    'status': usuario.aceptado,
                    'idCliente': usuario.idCliente,
                    'aceptado': usuario.aceptado,
                    'fondeado': usuario.fondeado,
                    'eliminado': usuario.eliminado,
                    'userTelegram': usuario.userTelegram,
                    'url_livecommunity': f'{url_livecommunity_base}{usuario.fpa}' if usuario.fpa else '',
                    'url_skilling': f'{url_skilling_base}{usuario.fpa}' if usuario.fpa else '',
                }
                for usuario in usuarios
            ]

            return JsonResponse({'data': data}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error al decodificar el JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método HTTP no válido'}, status=405)


@csrf_exempt   
def users_eliminados(request):
    if request.method == 'GET':
        try:
            usuarios = Usuario.objects.filter(eliminado=True)  # Filtrar usuarios eliminados
            urls = Url.objects.all()  # Obtenemos las URLs como en los otros métodos
            data = []

            for usuario in usuarios:
                # Creamos la lista de roles serializable
                roles = []
                for rol in usuario.roles.all():
                    roles.append({
                        'id': rol.rol_id,
                        'rol': rol.rol.name,
                        # 'fecha_asignacion': rol.fecha_asignacion.isoformat()
                    })

                # Creamos la lista de servicios serializable
                servicios = []
                for servicio in usuario.serviciosUsuario.all():
                    servicios.append({
                        'id': servicio.servicio_id,
                        'servicio': servicio.servicio.name
                    })

                # Creamos el diccionario de datos del usuario sin la contraseña
                user_data = {
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
                    'url_livecommunity': f'{urls[0].url}{usuario.fpa}' if usuario.fpa else '',
                    'url_skilling': f'{urls[1].url}{usuario.fpa}' if usuario.fpa else '',
                }

                data.append(user_data)

            # Devolvemos la lista de usuarios eliminados
            return JsonResponse({'data': data}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error al decodificar el JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método HTTP no válido'}, status=405)

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