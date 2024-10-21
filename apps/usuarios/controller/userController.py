from collections import defaultdict
from email.message import EmailMessage
import json
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from apps.api.skilling.models import Fpas
from livecommunity import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
import requests
import telegram
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
from django.core.mail import send_mail
from django.db import transaction
from django.conf import settings
from livecommunity.settings import TELEGRAM_BOT_TOKEN,CHAT_ID_BOT
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


chat_id = CHAT_ID_BOT
token = TELEGRAM_BOT_TOKEN



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
                    'up_line': usuario.up_line,
                    'link': usuario.link,
                    'roles': roles,
                    'servicios': servicios,
                    'registrado': usuario.registrado,
                    'status': usuario.aceptado,
                    'idSkilling': usuario.idSkilling,
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


def addfpas(request):
    try:
        response = requests.get("https://livecommunity.info/api/userNewFormat/")
        if response.status_code != 200:
            return JsonResponse({"message": "Error en la petición a la URL externa"}, status=response.status_code)

        external_data = response.json()
        usuarios_data = external_data.get("data", [])
        
        # Obtener todos los FPAs existentes de los usuarios externos
        fpas_existentes = set()
        for user_data in usuarios_data:
            fpa = user_data.get('fpa')
            if fpa:
                fpas_existentes.add(fpa)
        # Actualizar la tabla Fpas con los FPAs existentes
        for fpa in fpas_existentes:
            Fpas.objects.get_or_create(fpa=fpa)

        return JsonResponse({"message": "FPAs actualizados correctamente"}, status=200)
    except Exception as e:
        return JsonResponse({"message": f"Error al actualizar los FPAs: {str(e)}"}, status=500)



@csrf_exempt
@transaction.atomic
def postNewUsers(request):
    try:
        # Obtener datos externos
        response = requests.get("https://livecommunity.info/api/userNewFormat/")
        if response.status_code != 200:
            return JsonResponse({"message": "Error en la petición a la URL externa"}, status=response.status_code)

        external_data = response.json()
        usuarios_data = external_data.get("data", [])

        # Separar usuarios en socios y clientes
        socios_list = []
        clientes_list = []

        for user_data in usuarios_data:
            if user_data.get('fpa'):
                socios_list.append(user_data)
            elif user_data.get('idCliente'):
                clientes_list.append(user_data)
            else:
                # Opcional: manejar usuarios sin fpa y sin idCliente
                continue

        # Crear un diccionario de socios por email
        socios_by_email = {}
        for socio in socios_list:
            email = socio.get('email')
            if email:
                socios_by_email[email.lower()] = socio
            else:
                # Opcional: manejar socios sin email
                continue

        # Unificar datos de clientes que tienen el mismo email que un socio
        for cliente in clientes_list[:]:  # Copia para poder modificar la lista
            email = cliente.get('email')
            if email and email.lower() in socios_by_email:
                socio = socios_by_email[email.lower()]
                # Unificar datos, priorizando los del socio
                for key, value in cliente.items():
                    if value and not socio.get(key):
                        socio[key] = value
                # Remover cliente de la lista de clientes
                clientes_list.remove(cliente)

        # Preparar roles y servicios
        roles_dict = {rol.id: rol for rol in Rol.objects.filter(id__in=[2, 3])}
        servicios_dict = {servicio.id: servicio for servicio in Servicio.objects.filter(id__in=[1, 3])}

        nuevos_usuarios_creados = 0

        # Función para crear usuarios
        def crear_usuario(user_data, is_socio):
            email = user_data.get('email')
            if Usuario.objects.filter(email=email).exists():
                return  # Usuario ya existe

            base_username = user_data.get("email")
            registrado = user_data.get("registrado") or False
            aceptado = user_data.get("status") or False

            # Para clientes, generar fpa
            if not is_socio:
                up_line_value = user_data.get("uplink") or 'LA500S'
                fpa_data = getFpasForUser2(up_line_value)
                if fpa_data:
                    user_data['fpa'] = fpa_data.get('fpa_siguiente')
                    # Guardar el nuevo FPA en la tabla Fpas
                    Fpas.objects.create(fpa=user_data['fpa'])

            new_user = Usuario(
                username=base_username,
                fpa=user_data.get("fpa"),
                idSkilling=user_data.get("idCliente"),
                email=user_data.get("email"),
                first_name=user_data.get("nombre") or "",
                last_name=user_data.get("apellido") or "",
                telephone=user_data.get("telefono") or "",
                wallet=user_data.get("wallet") or "",
                up_line=user_data.get("uplink") or "",
                link=user_data.get("link") or "https://livecommunity.info/Afiliado/",
                registrado=registrado,
                aceptado=aceptado,
                userTelegram=user_data.get("userTelegram") or "",
                nacionalidad=user_data.get("nacionalidad") or "",
            )

            # Establecer la contraseña "123456"
            new_user.set_password("123456")

            # Guardar el usuario
            new_user.save()
            nonlocal nuevos_usuarios_creados
            nuevos_usuarios_creados += 1

            # Asignar roles y servicios
            if is_socio:
                # Socio: rol [2], servicios [1, 3]
                if 2 in roles_dict:
                    UsuarioRol.objects.create(usuario=new_user, rol=roles_dict[2])
            else:
                # Cliente: rol [3], servicios [1, 3]
                if 3 in roles_dict:
                    UsuarioRol.objects.create(usuario=new_user, rol=roles_dict[3])

            # Asignar servicios [1, 3]
            for servicio_id in [1, 3]:
                if servicio_id in servicios_dict:
                    UsuarioServicio.objects.create(usuario=new_user, servicio=servicios_dict[servicio_id])

            # Actualizar FPA si es necesario
            if new_user.fpa:
                Fpas.objects.get_or_create(fpa=new_user.fpa)

        # Crear usuarios socios
        for socio_data in socios_list:
            crear_usuario(socio_data, is_socio=True)

        # Crear usuarios clientes
        for cliente_data in clientes_list:
            crear_usuario(cliente_data, is_socio=False)

        return JsonResponse({"message": f"Se crearon {nuevos_usuarios_creados} usuarios nuevos"}, status=200)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"message": f"Error de conexión: {str(e)}"}, status=500)
    except json.JSONDecodeError:
        return JsonResponse({"message": "Error al decodificar el JSON"}, status=403)
    except Exception as e:
        import traceback
        traceback_str = ''.join(traceback.format_tb(e.__traceback__))
        return JsonResponse({"message": f"Error inesperado: {str(e)}", "traceback": traceback_str}, status=500)


###############################################
#
#Codigo en modificacion
#
###############################################

@csrf_exempt
def postNewUser(request):
    if request.method == 'POST':
        if 'application/json' in request.content_type:
            try:
                user_data = json.loads(request.body)
                # Decodificar el cuerpo de la solicitud como JSON
                url = f"https://go.skillingpartners.com/api/?command=registrations&fromdate=&todate=&daterange=update&userid=skilling-{user_data.get("idSkilling")}&json=1"
                headers = {
                    'x-api-key': settings.SKILLING_API_KEY,
                    'affiliateid': '35881',
                }
                
                try:
                    response = requests.get(url, headers=headers)
                    response.raise_for_status()  # Esto lanzará una excepción para códigos de estado HTTP no exitosos
                    
                    # Intentar decodificar la respuesta JSON
                    
                    json_response = response.json()
                    
                    
                     
                except requests.RequestException as e:
                    return JsonResponse({'error':'usuario no registrado en skilling'}, status=500)
                
                
                fpa_up_line = json_response.get('registrations')[0]['Tracking_Code']
                
                
                fpas = Fpas.objects.all()
                Url.objects.all()
                
                url_skilling_base = Url.objects.get(id=2).url
                url_livecommunity_base = Url.objects.get(id=1).url
                
                pk = fpa_up_line.split(',')[0][:2]
                
                # Agrupamos los FPAs por su letra final
                fpas_dict = defaultdict(list)
                for fpa in fpas:
                    if fpa.fpa and fpa.fpa.startswith(pk):
                        fpas_dict[fpa.fpa[-1]].append(fpa.fpa)
                
                # Ordenamos cada lista de FPAs
                for letra in fpas_dict:
                    fpas_dict[letra].sort()
                
                def encontrar_siguiente(fpas_list, sufijo):
                    if not fpas_list:
                        return f"{pk}001{sufijo}"
                    for i in range(len(fpas_list) - 1):
                        actual = int(fpas_list[i][2:5])
                        siguiente = int(fpas_list[i+1][2:5])
                        if siguiente - actual > 1:
                            return f"{pk}{actual+1:03d}{sufijo}"
                    ultimo = int(fpas_list[-1][2:5])
                    return f"{pk}{ultimo+1:03d}{sufijo}"

                siguientes_faltantes = {letra: encontrar_siguiente(fpas, 'S') for letra, fpas in fpas_dict.items()}
                
                # Encontrar el menor siguiente faltante
                siguiente_faltante = min(siguientes_faltantes.values())

                # Combinar todas las listas de FPAs
                todos_fpas = sorted([fpa for fpas in fpas_dict.values() for fpa in fpas])
                
                
                
                Fpas.objects.get_or_create(
                    fpa=siguiente_faltante
                )
                
                
                # Generar el username a partir del apellido y nombre
                try:
                    base_username = (user_data.get("last_name") + "_" + user_data.get("first_name")).replace(" ", "_")
                except Exception as e:
                    print(f"Error generando el username: {e}")
                    return JsonResponse({"message": "Error al crear el usuario"}, status=400)

                try:# Verificar si el usuario con ese username ya existe
                    existing_user = Usuario.objects.get(fpa=user_data.get("idSkilling"),email=user_data.get("email"))
                    return JsonResponse({"message": "Usuario ya existe"}, status=404)
                except Usuario.DoesNotExist:
                    pass

                
                new_user = Usuario(
                    username=base_username,
                    fpa=siguiente_faltante,
                    idSkilling=user_data.get("idSkilling") or None,
                    email=user_data.get("email"),
                    first_name=user_data.get("first_name"),
                    last_name=user_data.get("last_name"),
                    telephone=user_data.get("telephone"),
                    wallet=user_data.get("wallet"),
                    up_line=fpa_up_line,
                    link=user_data.get("link") or "https://livecommunity.info/Afiliado/",
                    registrado=user_data.get("registrado", False) if user_data.get("registrado") is not None else False,
                    aceptado=user_data.get("status", False) if user_data.get("status") is not None else False,
                    userTelegram=user_data.get("userTelegram") or None,
                    userDiscord=user_data.get("userDiscord") or None,
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
                    
                    
                    enviar_correo(user_data.get("first_name"), user_data.get("telefono"), user_data.get("email"), user_data.get("idSkilling"), user_data.get("password"),siguiente_faltante)
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
                'up_line': usuario.up_line,
                'link': usuario.link,
                'roles': roles,
                'servicios': servicios,
                'registrado': usuario.registrado,
                'status': usuario.aceptado,
                'idSkilling': usuario.idSkilling,
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


@csrf_exempt  
def users(request):
    if request.method == 'GET':
        try:
            # Prefetch para evitar consultas adicionales
            usuarios: list[Usuario] = Usuario.objects.all().prefetch_related('roles__rol', 'serviciosUsuario')
            # Solo obtener las URLs necesarias, si son las primeras dos
            urls: list[Url] = Url.objects.all()[:2]
            
            url_livecommunity_base = urls[0].url if len(urls) > 0 else ''
            url_skilling_base = urls[1].url if len(urls) > 1 else ''
            
            # List comprehension para generar la respuesta
            data = [
                {
                    'fpa': usuario.fpa,
                    'email': usuario.email,
                    'first_name': usuario.first_name,
                    'last_name': usuario.last_name,
                    'telephone': usuario.telephone,
                    'wallet': usuario.wallet,
                    'up_line': usuario.up_line,
                    'link': usuario.link,
                    'roles': [{'id': rol.rol_id, 'rol': rol.rol.name} for rol in usuario.roles.all()],  # Cambiamos a rol.rol.name
                    'servicios': [{'id': servicio.servicio_id, 'servicio': servicio.servicio.name} for servicio in usuario.serviciosUsuario.all()],
                    'registrado': usuario.registrado,
                    'status': usuario.aceptado,
                    'idSkilling': usuario.idSkilling,
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
            print(f"Error en users: {e}")
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
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserById(request, pk):
    try:
        usuario = Usuario.objects.get(fpa=pk)
        url_skilling_base = Url.objects.get(id=2).url
        url_livecommunity_base = Url.objects.get(id=1).url
        

        if request.method in ['POST', 'PUT']:
            try:
                body_data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'message': 'Datos inválidos en el cuerpo (body)'}, status=400)

            # Actualiza los datos básicos del usuario
            for field in ['first_name', 'last_name', 'email', 'telephone', 'wallet']:
                if field in body_data:
                    setattr(usuario, field, body_data[field])
            
            if 'status' in body_data:
                usuario.aceptado = body_data['status']

            # Verifica si el usuario tenía el rol de Socio antes de la actualización
            tenia_rol_socio = usuario.roles.filter(id=2).exists()

            # Actualiza los roles si se proporcionaron
            if 'roles' in body_data:
                UsuarioRol.objects.filter(usuario=usuario).delete()
                tiene_rol_socio_ahora = False

                for rol_data in body_data['roles']:
                    rol = Rol.objects.get(id=rol_data['id'])
                    UsuarioRol.objects.create(usuario=usuario, rol=rol)
                    if rol.id == 2:  # Asumiendo que el ID 2 corresponde al rol de Socio
                        tiene_rol_socio_ahora = True

                # Si no tenía el rol de Socio antes y ahora sí, envía el correo
                if not tenia_rol_socio and tiene_rol_socio_ahora:
                    enviar_correo_socio(nombre=usuario.first_name, telefono=usuario.telephone, correo=usuario.email, id_cliente=usuario.idSkilling, fpa=usuario.fpa, url_live=url_livecommunity_base, url_skilling=url_skilling_base)  # Asegúrate de que esta función esté definida e importada

            # Actualiza los servicios si se proporcionaron
            if 'servicios' in body_data:
                UsuarioServicio.objects.filter(usuario=usuario).delete()
                for servicio_data in body_data['servicios']:
                    servicio = Servicio.objects.get(id=servicio_data['id'])
                    UsuarioServicio.objects.create(usuario=usuario, servicio=servicio)

            usuario.save()

            # Prepara los datos para la respuesta
            roles = [
                {
                    'id': rol.rol_id,
                    'rol': rol.rol.name,
                    'fecha_asignacion': rol.fecha_asignacion.isoformat()
                } for rol in usuario.roles.all()
            ]

            servicios = [
                {
                    'id': servicio.servicio_id,
                    'servicio': servicio.servicio.name
                } for servicio in usuario.serviciosUsuario.all()
            ]

            data = {
                'fpa': usuario.fpa,
                'email': usuario.email,
                'first_name': usuario.first_name,
                'telephone': usuario.telephone,
                'wallet': usuario.wallet,
                'up_line': usuario.up_line,
                'link': usuario.link,
                'roles': roles,
                'servicios': servicios,
                'registrado': usuario.registrado,
                'status': usuario.aceptado,
                'idSkilling': usuario.idSkilling,
                'aceptado': usuario.aceptado,
                'fondeado': usuario.fondeado,
                'eliminado': usuario.eliminado,
                'userTelegram': usuario.userTelegram,
            }

            return JsonResponse({'data': data}, status=200)

    except Usuario.DoesNotExist:
        return JsonResponse({'message': 'Usuario no encontrado'}, status=404)

    return JsonResponse({'message': 'Método HTTP no válido'}, status=405)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
                'up_line': users.up_line,
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
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
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
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminarUserForever(request, pk):
    print('eliminarUserForever: Started')
    if request.method == 'DELETE':
        try:
            print('eliminarUserForever: DELETE method')
            # Obtener el usuario por su pk (fpa)
            user = get_object_or_404(Usuario, fpa=pk)
            print(f'eliminarUserForever: User {user} found')
            
            # Eliminar el usuario permanentemente de la base de datos
            user.delete()
            print('eliminarUserForever: User deleted')
            
            response = JsonResponse({'data': 'Usuario eliminado permanentemente'}, status=200)
        except Exception as e:
            print(f'eliminarUserForever: Exception {e}')
            response = JsonResponse({'error': str(e)}, status=500)
    else:
        print('eliminarUserForever: Invalid method')
        response = JsonResponse({'error':'Método no válido'}, status=405)

    print('eliminarUserForever: Finished')
    return response


@csrf_exempt  
# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
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
@api_view(['POST'])
@permission_classes([IsAuthenticated])
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


def getRoles(request):
    if request.method == 'GET':
        # Obtenemos todos los roles
        roles = Rol.objects.all()

        # Convertimos el queryset a una lista de diccionarios
        roles_list = [
            {
                'id': rol.id,
                'name': rol.name,
            }
            for rol in roles
        ]

        # Devolvemos la lista serializada en formato JSON
        return JsonResponse({'data': roles_list}, status=200)
    else:
        return JsonResponse({'Error': 'Metodo HTTP incorrecto'}, status=405)

def getServicios(request):
    if request.method == 'GET':
        # Obtenemos todos los servicios
        servicios = Servicio.objects.all()

        # Convertimos el queryset a una lista de diccionarios
        servicios_list = [
            {
                'id': servicio.id,
                'name': servicio.name,
            }
            for servicio in servicios
        ]

        # Devolvemos la lista serializada en formato JSON
        return JsonResponse({'data': servicios_list}, status=200)
    else:
        return JsonResponse({'Error': 'Metodo HTTP incorrecto'}, status=405)



# def getFpasForUser(request, pk):
#     if request.method == 'GET':
#         # Obtenemos todos los fpas
#         fpas = Fpas.objects.all()
#         Url.objects.all()
        
#         url_skilling_base = Url.objects.get(id=2).url
#         url_livecommunity_base = Url.objects.get(id=1).url
        
#         pk = pk.split(',')[0][:2]
        
#         # Agrupamos los FPAs por su letra final
#         fpas_dict = defaultdict(list)
#         for fpa in fpas:
#             if fpa.fpa and fpa.fpa.startswith(pk):
#                 fpas_dict[fpa.fpa[-1]].append(fpa.fpa)
        
#         # Ordenamos cada lista de FPAs
#         for letra in fpas_dict:
#             fpas_dict[letra].sort()
        
#         def encontrar_siguiente(fpas_list, sufijo):
#             if not fpas_list:
#                 return f"{pk}001{sufijo}"
#             for i in range(len(fpas_list) - 1):
#                 actual = int(fpas_list[i][2:5])
#                 siguiente = int(fpas_list[i+1][2:5])
#                 if siguiente - actual > 1:
#                     return f"{pk}{actual+1:03d}{sufijo}"
#             ultimo = int(fpas_list[-1][2:5])
#             return f"{pk}{ultimo+1:03d}{sufijo}"

#         siguientes_faltantes = {letra: encontrar_siguiente(fpas, letra) for letra, fpas in fpas_dict.items()}
        
#         # Encontrar el menor siguiente faltante
#         siguiente_faltante = min(siguientes_faltantes.values())

#         # Combinar todas las listas de FPAs
#         todos_fpas = sorted([fpa for fpas in fpas_dict.values() for fpa in fpas])
        
#         # Fpas.objects.get_or_create(
#         #     fpa=siguiente_faltante
#         # )

#         return JsonResponse({
#             # 'data': todos_fpas,
#             'fpa_siguiente': siguiente_faltante,
#             'url_skilling': f'{url_skilling_base}{siguiente_faltante}',
#             'url_livecommunity': f'{url_livecommunity_base}{siguiente_faltante}'
#         }, status=200)
#     else:
#         return JsonResponse({'Error': 'Método HTTP incorrecto'}, status=405)
    

@transaction.atomic
def registrar_usuario(request, pk):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.POST.get('first_name').strip()
        apellido = request.POST.get('last_name').strip()
        email = request.POST.get('email').strip()
        telefono = request.POST.get('telephone').strip()
        fpa_up_line = request.POST.get('fpa').strip()
        userTelegram = request.POST.get('userTelegram').strip()
        userDiscord = request.POST.get('userDiscord').strip()
        documento = request.POST.get('documento').strip()
        file = request.FILES.get('file')
        file2 = request.FILES.get('file2')
        wallet = request.POST.get('wallet').strip()
        nacionalidad = request.POST.get('nacionalidad').strip()
        
        
        existe_user = Usuario.objects.filter(email=email).exists()
        if existe_user:
            return render(request, 'registro.html', {'error': 'El usuario ya existe'})
        
        
        fpa_get_data  = getFpasForUser(fpa_up_line)
        url_skilling = fpa_get_data.get('url_skilling')
        url_livecommunity = fpa_get_data.get('url_livecommunity')
        
        fpa_skilling = fpa_get_data.get('fpa_siguiente')
        Fpas.objects.get_or_create(fpa=fpa_skilling)
        print(fpa_skilling)
        
        # Generar una contraseña temporal
        temp_password = Usuario.objects.make_random_password()

        new_user = Usuario(
            username=email,
            fpa=fpa_skilling,
            idSkilling=None,
            email=email,
            first_name=nombre,
            last_name=apellido,
            documento=documento,
            telephone=telefono,
            wallet=wallet,
            up_line=fpa_up_line,
            link=None,
            registrado=False,
            aceptado=False,
            userTelegram=userTelegram,
            userDiscord=userDiscord,
            nacionalidad=nacionalidad,
        )
        new_user.set_password(temp_password)
        
        try:
            # Guardar el nuevo usuario en la base de datos  
            new_user.save()
            # Asignar roles al nuevo usuario
            roles = [3]
            for rol_id in roles:
                try:
                    rol = Rol.objects.get(id=rol_id)
                    UsuarioRol.objects.create(usuario=new_user, rol=rol)
                except Rol.DoesNotExist:
                    return JsonResponse({"message": f"Rol con ID {rol_id} no existe"}, status=400)
            # Asignar servicios al nuevo usuario
            servicios = [1]
            for servicio_id in servicios:
                try:
                    servicio = Servicio.objects.get(id=servicio_id)
                    UsuarioServicio.objects.create(usuario=new_user, servicio=servicio)
                except Servicio.DoesNotExist:
                    return JsonResponse({"message": f"Servicio con ID {servicio_id} no existe"}, status=400)
            
            
            # Enviar correo con los datos del nuevo usuario
            try:
                enviar_correo_new_user(
                    nombre=new_user.first_name,
                    telefono=new_user.telephone,
                    correo=new_user.email,
                    id_cliente=new_user.idSkilling,
                    password_temporal=temp_password,
                    fpa=new_user.fpa,
                fpa_up_line=new_user.up_line,
                username=new_user.username
                )
            except Exception as e:
                print(f"Error enviando el correo: {e}")
            
            files = [file] if file else []
            if file2:
                files.append(file2)
            try:
                enviar_correo_email_admin(
                    usuario=new_user,
                    files=files
                )
                
            except Exception as e:
                print(f"Error enviando el correo: {e}")
            
            
            
            return render(request, 'brokerSelecte.html', {'fpa': pk})
        except Exception as e:
            print(f"Error guardando el usuario {new_user.username}: {e}")
            return render(request, 'registro.html', {'error': f"Error guardando el usuario: {e}"})






@csrf_exempt
def asociar_documento_con_idSkilling(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y analizarlo como JSON
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            idSkilling = body_data.get('idSkilling')
            documento = body_data.get('documento')
            servicio_body = body_data.get('servicio')
            
            try:
                usuario = Usuario.objects.get(documento=documento)
            except Usuario.DoesNotExist:
                return JsonResponse({'Error': 'Usuario no encontrado'}, status=404)
            
            try:
                usuario_con_idSkilling = Usuario.objects.get(idSkilling=idSkilling)
                if usuario_con_idSkilling:
                    return JsonResponse({'Error': 'El usuario ya tiene un idSkilling asociado'}, status=400)
            except Usuario.DoesNotExist:
                pass
            
            
            if usuario.idSkilling != None:
                print('El usuario ya tiene un idSkilling asociado')
                return JsonResponse({'Error': 'El usuario ya tiene un idSkilling asociado'}, status=400)
            
            
            usuario.idSkilling = idSkilling
            usuario.save()
            
            # Obtener los servicios actuales del usuario
            servicios_actuales = set(UsuarioServicio.objects.filter(usuario=usuario).values_list('servicio_id', flat=True))

            # Nuevo servicio a agregar
            nuevo_servicio_id = servicio_body # O el ID del servicio que quieras agregar

            # Verificar si el nuevo servicio ya existe para el usuario
            if nuevo_servicio_id not in servicios_actuales:
                try:
                    servicio = Servicio.objects.get(id=nuevo_servicio_id)
                    UsuarioServicio.objects.create(usuario=usuario, servicio=servicio)
                    print(f"Servicio con ID {nuevo_servicio_id} agregado al usuario.")
                except Servicio.DoesNotExist:
                    print(f"Servicio con ID {nuevo_servicio_id} no existe")
            else:
                print(f"El usuario ya tiene el servicio con ID {nuevo_servicio_id}")
            
            # Mensaje formateado para telegram
            # mensaje = f"Nombre: {nombre}\nApellido: {apellido}\nUser Telegram: {userTelegram}\nEmail: {new_user.email}\nTeléfono: {new_user.telephone}\nID Socio1: {fpa_skilling}\nID Socio2: {fpa_up_line}\nID Cliente: {new_user.idSkilling} \nUser Discord: {new_user.userDiscord}"
        
            # try:
            #     enviar_mensaje_sync(mensaje, chat_id, token)
            # except Exception as e:
            #     print(e.__str__())
            
            
            print(idSkilling, documento)
            return JsonResponse({'data': f'{idSkilling} - {documento}'})
        except json.JSONDecodeError:
            return JsonResponse({'Error': 'Datos JSON inválidos'}, status=400)
        except Exception as e:
            print(e.__str__())
            return JsonResponse({'Error': str(e)}, status=500)
    else:
        return JsonResponse({'Error': 'Método inválido'}, status=405)
    
    
############################################################################################
########################### METODOS ########################################################
############################################################################################

# Función para enviar correo con contraseña temporal (implementar según tus necesidades)
def enviar_correo_new_user(nombre, telefono, correo, id_cliente, password_temporal, fpa, fpa_up_line, username):
    asunto = 'Bienvenido a LiveCommunity - Información de tu cuenta'
    mensaje = f"""
    Hola {nombre},

    ¡Bienvenido a LiveCommunity! Tu cuenta ha sido creada exitosamente.

    Aquí están los detalles de tu cuenta:
    
    Nombre: {nombre}
    Teléfono: {telefono}
    Correo electrónico: {correo}
    Nombre de usuario: {username}
    ID de Cliente: {id_cliente}
    FPA: {fpa}
    FPA de tu upline: {fpa_up_line}
    
    Tu contraseña temporal es: {password_temporal}
    
    Por favor, ingresa a nuestra plataforma (https://www.livecommunity.xyz/) y cambia tu contraseña lo antes posible.

    Pasos para cambiar tu contraseña:
    1. Accede a la plataforma con tu nombre de usuario y contraseña temporal.
    2. Ve a la sección de "Perfil" o "Configuración de cuenta".
    3. Busca la opción "Cambiar contraseña" y sigue las instrucciones.

    Si tienes alguna pregunta o necesitas ayuda, no dudes en contactarnos.

    ¡Gracias por unirte a LiveCommunity! Estamos emocionados de tenerte con nosotros.

    Saludos,
    El equipo de LiveCommunity
    """
    
    lista_destinatarios = [correo]  # Enviamos el correo al usuario
    correo_remitente = settings.EMAIL_HOST_USER

    try:
        send_mail(asunto, mensaje, correo_remitente, lista_destinatarios, fail_silently=False)
        print(f"Correo enviado exitosamente a {correo}")
        return True
    except Exception as e:
        print(f"Error al enviar el correo: {str(e)}")
        return False






def enviar_correo_email_admin(usuario, files=None):
    asunto = 'Bienvenido a LiveCommunity - Información de tu cuenta'
    mensaje = f"""
    Hola {usuario.first_name},

    ¡Bienvenido a LiveCommunity! Tu cuenta ha sido creada exitosamente.

    Aquí están los detalles de tu cuenta:

    Nombre completo: {usuario.first_name} {usuario.last_name}
    Teléfono: {usuario.telephone}
    Correo electrónico: {usuario.email}
    Nombre de usuario: {usuario.username}
    ID de Cliente: {usuario.idSkilling}
    FPA: {usuario.fpa}
    FPA de tu upline: {usuario.up_line}
    Documento: {usuario.documento}
    Nacionalidad: {usuario.nacionalidad}
    Wallet: {usuario.wallet}
    Usuario de Telegram: {usuario.userTelegram}
    Usuario de Discord: {usuario.userDiscord}

    Por favor, ingresa a nuestra plataforma (https://www.livecommunity.xyz/) y cambia tu contraseña lo antes posible.

    Pasos para cambiar tu contraseña:
    1. Accede a la plataforma con tu nombre de usuario y contraseña temporal.
    2. Ve a la sección de "Perfil" o "Configuración de cuenta".
    3. Busca la opción "Cambiar contraseña" y sigue las instrucciones.

    Si tienes alguna pregunta o necesitas ayuda, no dudes en contactarnos.

    ¡Gracias por unirte a LiveCommunity! Estamos emocionados de tenerte con nosotros.

    Saludos,
    El equipo de LiveCommunity
    """

    # Lista de destinatarios
    lista_destinatarios = ['pascualsilvestri14@gmail.com']
    
    try:
        # Crear el mensaje
        email = EmailMessage(
            subject=asunto,
            body=mensaje,
            from_email=settings.EMAIL_HOST_USER,
            to=lista_destinatarios
        )
        
        # Adjuntar archivos si existen
        if files:
            if not isinstance(files, list):
                files = [files]
            for file in files:
                email.attach(file.name, file.read(), file.content_type)

        # Enviar el correo
        email.send()

        print(f"Correo enviado exitosamente a {usuario.email}")
        return True
    except Exception as e:
        print(f"Error al enviar el correo: {str(e)}")
        return False
    
    
    
    
    
def enviar_correo_socio(nombre, telefono, correo, id_cliente, fpa, url_live, url_skilling):
    asunto = 'Bienvenido a liveAcademy - Información de tu cuenta'
    mensaje = f"""
    Hola {nombre},

    ¡Bienvenido a liveAcademy! 
    
    Ahora como nuevo socio de liveAcademy, puedes acceder a la dashboard de tu cuenta.
    
    https://www.livecommunity.xyz/
    
    Aquí están los detalles de tu cuenta:
    
    Nombre: {nombre}
    Teléfono: {telefono}
    Correo electrónico: {correo}
    ID de Cliente: {id_cliente}
    Fpa: {fpa}
    
    Tu url de liveAcademy es: {url_live}{fpa}
    Tu url de skilling es: {url_skilling}{fpa}

    Si tienes alguna pregunta o necesitas ayuda, no dudes en contactarnos.

    ¡Gracias por unirte a LiveCommunity!

    Saludos,
    El equipo de liveAcademy
    """
    
    lista_destinatarios = [correo]  # Enviamos el correo al usuario
    correo_remitente = settings.EMAIL_HOST_USER

    try:
        send_mail(asunto, mensaje, correo_remitente, lista_destinatarios, fail_silently=False)
        print(f"Correo enviado exitosamente a {correo}")
        return True
    except Exception as e:
        print(f"Error al enviar el correo: {str(e)}")
        return False

def getFpasForUser2(fpaSkilling):
    fpas = Fpas.objects.all()
    
    url_skilling_base = Url.objects.get(id=2).url
    url_livecommunity_base = Url.objects.get(id=1).url
    
    # Intentar obtener el prefijo del up_line_value
    pk = fpaSkilling.split(',')[0][:2]
    
    # Filtrar FPAs que empiezan con 'pk'
    fpas_con_pk = [fpa.fpa for fpa in fpas if fpa.fpa and fpa.fpa.startswith(pk)]
    
    if not fpas_con_pk:
        # Si no hay FPAs con el prefijo 'pk', usar 'LA' como prefijo
        pk = 'LA'
        fpas_con_pk = [fpa.fpa for fpa in fpas if fpa.fpa and fpa.fpa.startswith(pk)]
    
    # Ahora, agrupar los FPAs existentes por su letra final
    fpas_dict = defaultdict(list)
    for fpa in fpas_con_pk:
        fpas_dict[fpa[-1]].append(fpa)
    
    # Ordenamos cada lista de FPAs
    for letra in fpas_dict:
        fpas_dict[letra].sort()
    
    def encontrar_siguiente(fpas_list, sufijo):
        if not fpas_list:
            return f"{pk}001{sufijo}"
        for i in range(len(fpas_list) - 1):
            actual = int(fpas_list[i][2:5])
            siguiente = int(fpas_list[i+1][2:5])
            if siguiente - actual > 1:
                return f"{pk}{actual+1:03d}{sufijo}"
        ultimo = int(fpas_list[-1][2:5])
        return f"{pk}{ultimo+1:03d}{sufijo}"
    
    siguientes_faltantes = {letra: encontrar_siguiente(fpas_list, letra) for letra, fpas_list in fpas_dict.items()}
    
    if siguientes_faltantes:
        siguiente_faltante = min(siguientes_faltantes.values())
    else:
        # Si aún no hay FPAs, creamos el primero con sufijo 'S'
        siguiente_faltante = f"{pk}001S"
    
    # Combinar todas las listas de FPAs
    todos_fpas = sorted([fpa for fpas_list in fpas_dict.values() for fpa in fpas_list])
    
    return {
        'data': todos_fpas,
        'fpa_siguiente': siguiente_faltante,
        'url_skilling': f'{url_skilling_base}{siguiente_faltante}',
        'url_livecommunity': f'{url_livecommunity_base}{siguiente_faltante}'
    }


def getFpasForUser(fpaSkilling):
    fpas = Fpas.objects.all()
    Url.objects.all()
    
    url_skilling_base = Url.objects.get(id=2).url
    url_livecommunity_base = Url.objects.get(id=1).url
    
    pk = fpaSkilling.split(',')[0][:2]
    
    # Agrupamos los FPAs por su letra final
    fpas_dict = defaultdict(list)
    for fpa in fpas:
        if fpa.fpa and fpa.fpa.startswith(pk):
            fpas_dict[fpa.fpa[-1]].append(fpa.fpa)
    
    # Ordenamos cada lista de FPAs
    for letra in fpas_dict:
        fpas_dict[letra].sort()
    
    def encontrar_siguiente(fpas_list, sufijo):
        if not fpas_list:
            return f"{pk}001{sufijo}"
        for i in range(len(fpas_list) - 1):
            actual = int(fpas_list[i][2:5])
            siguiente = int(fpas_list[i+1][2:5])
            if siguiente - actual > 1:
                return f"{pk}{actual+1:03d}{sufijo}"
        ultimo = int(fpas_list[-1][2:5])
        return f"{pk}{ultimo+1:03d}{sufijo}"
    siguientes_faltantes = {letra: encontrar_siguiente(fpas, letra) for letra, fpas in fpas_dict.items()}
    
    # Encontrar el menor siguiente faltante
    siguiente_faltante = min(siguientes_faltantes.values())
    # Combinar todas las listas de FPAs
    todos_fpas = sorted([fpa for fpas in fpas_dict.values() for fpa in fpas])
    
    # Fpas.objects.get_or_create(
    #     fpa=siguiente_faltante
    # )
    return {
        'data': todos_fpas,
        'fpa_siguiente': siguiente_faltante,
        'url_skilling': f'{url_skilling_base}{siguiente_faltante}',
        'url_livecommunity': f'{url_livecommunity_base}{siguiente_faltante}'
    }


        
#Envio de mensaje a hacia telegram
def enviar_mensaje_sync(msj, id, token):
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=id, text=msj)




# MessageString = 'hola'
# print(MessageString)
# asyncio.run(enviar_mensaje(MessageString, chat_id, token))
    
@csrf_exempt
def post_roles_servicios_user(request):
    if request.method == 'POST':
        try:
            roles = ['admin', 'socio', 'cliente', 'moderador']
            servicios = ['free', 'pro', 'skilling']
            
            for rol in roles:
                rol, created = Rol.objects.get_or_create(name=rol)
                
            for servicio in servicios:
                servicio, created = Servicio.objects.get_or_create(name=servicio)   
                
            return JsonResponse({"message": "Roles y servicios creados exitosamente"}, status=200)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)
    else:
        return JsonResponse({"message": "Método no permitido"}, status=405)
                
                
