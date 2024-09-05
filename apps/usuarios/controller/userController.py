import json
from django.http import JsonResponse
import requests
from apps.api.skilling.models import Afiliado
from apps.usuarios.models import (
    Rol,
    Servicio,
    Usuario,
    UsuarioRol,
    UsuarioServicio,
    Url,
    UsuarioUrl
)
from django.views.decorators.csrf import csrf_exempt


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
                    servicios = user_data.get("servicios", [])  # Lista de IDs de servicios
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

                        # Crear URLs si FPA no es None
                        if new_user.fpa:
                            try:
                                Url.objects.create(
                                    name="Afiliado URL",
                                    url=f"https://livecommunity.info/Afiliado/{new_user.fpa}",
                                    usuario=new_user,
                                    
                                )
                                Url.objects.create(
                                    name="Skilling Partners URL",
                                    url=f"https://go.skillingpartners.com/visit/?bta=35881&nci=5846&utm_campaign={new_user.fpa}",
                                    usuario=new_user,
                                    
                                )
                            except Exception as e:
                                print(f"Error creando URLs para {new_user.username}: {e}")

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
                        first_name=user_data.get("nombre"),
                        last_name=user_data.get("apellido"),
                        telephone=user_data.get("telefono"),
                        wallet=user_data.get("wallet"),
                        uplink=user_data.get("uplink") or "",
                        link=user_data.get("link") or "https://livecommunity.info/Afiliado/",
                        registrado=user_data.get("registrado", False) if user_data.get("registrado") is not None else False,
                        aceptado=user_data.get("status", False) if user_data.get("status") is not None else False,
                        userTelegram=user_data.get("userTelegram") or None,
                    )

                    # Hashear y establecer la contraseña del nuevo usuario
                    if user_data.get("password"):
                        new_user.set_password(user_data.get("password"))
                    else:
                        # Opción para manejar una contraseña por defecto si no se proporciona una
                        new_user.set_password("default_password")

                    try:
                        # Guardar el nuevo usuario en la base de datos
                        new_user.save()

                        # Crear URLs si FPA no es None
                        if new_user.fpa:
                            try:
                                Url.objects.create(
                                    name="Afiliado URL",
                                    url=f"https://livecommunity.info/Afiliado/{new_user.fpa}",
                                    usuario=new_user,
                                )
                                Url.objects.create(
                                    name="Skilling Partners URL",
                                    url=f"https://go.skillingpartners.com/visit/?bta=35881&nci=5846&utm_campaign={new_user.fpa}",
                                    usuario=new_user,
                                )
                            except Exception as e:
                                print(f"Error creando URLs para {new_user.username}: {e}")

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
    
    
def createUser(request):
    try:
        # Extraer los datos de la solicitud
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        fpa = request.POST.get("fpa")
        idCliente = request.POST.get("idCliente")
        telephone = request.POST.get("telephone")
        userTelegram = request.POST.get("userTelegram", "none")
        registrado = request.POST.get("registrado", False)
        aceptado = request.POST.get("aceptado", False)
        fondeado = request.POST.get("fondeado", False)
        eliminado = request.POST.get("eliminado", False)

        # Recibir roles y servicios como listas de IDs (o nombres)
        roles = request.POST.getlist("roles")  # Lista de IDs o nombres de roles
        servicios = request.POST.getlist(
            "servicios"
        )  # Lista de IDs o nombres de servicios

        # Validar que se tengan los campos obligatorios
        if not username or not password or not email:
            return JsonResponse(
                {
                    "error": "El nombre de usuario, contraseña y correo electrónico son obligatorios."
                },
                status=400,
            )

        # Crear el usuario con los campos proporcionados
        new_user = Usuario.objects.create(
            username=username,
            password=password,  # Almacenar la contraseña de forma segura
            email=email,
            fpa=fpa,
            idCliente=idCliente,
            telephone=telephone,
            userTelegram=userTelegram,
            registrado=registrado,
            aceptado=aceptado,
            fondeado=fondeado,
            eliminado=eliminado,
        )

        # Asignar roles si existen
        if roles:
            for rol_id in roles:
                try:
                    rol = Rol.objects.get(id=rol_id)  # Buscar el rol por ID
                    UsuarioRol.objects.create(
                        usuario=new_user, rol=rol
                    )  # Relación ManyToMany
                except Rol.DoesNotExist:
                    return JsonResponse(
                        {"error": f"El rol con id {rol_id} no existe."}, status=400
                    )

        # Asignar servicios si existen
        if servicios:
            for servicio_id in servicios:
                try:
                    servicio = Servicio.objects.get(
                        id=servicio_id
                    )  # Buscar el servicio por ID
                    UsuarioServicio.objects.create(
                        usuario=new_user, servicio=servicio
                    )  # Relación ManyToMany
                except Servicio.DoesNotExist:
                    return JsonResponse(
                        {"error": f"El servicio con id {servicio_id} no existe."},
                        status=400,
                    )

        # Guardar el usuario en la base de datos
        new_user.save()

        # Retornar una respuesta exitosa
        return JsonResponse(
            {"message": "Usuario creado exitosamente", "usuario": new_user.username}
        )

    except Exception as e:
        # En caso de error, retornar un mensaje de error
        return JsonResponse({"error": str(e)}, status=500)


def users(request):
    usuarios = Usuario.objects.all()
    rolesAndUsuario = []
    for usuario in usuarios:
        roles = []
        servicios = []
        for rol in usuario.roles_asignados.all():
            roles.append(rol.name)

        for servicio in usuario.servicios_asignados.all():
            servicios.append(servicio.name)

        rolesAndUsuario.append(
            {"username": usuario.username, "roles": roles, "servicios": servicios}
        )

    return JsonResponse({"users": rolesAndUsuario})
