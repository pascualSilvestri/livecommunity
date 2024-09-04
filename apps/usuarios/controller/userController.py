import json
from django.http import JsonResponse
import requests
from apps.afiliado.models import Afiliado
from apps.usuarios.models import (
    Rol,
    Servicio,
    TipoUrl,
    Usuario,
    UsuarioRol,
    UsuarioServicio,
    Url,
)
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def postNewUser(request):
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
                # Verificar si ya existe un usuario con el FPA proporcionado
                if Usuario.objects.filter(fpa=user_data.get("fpa")).exists():
                    continue  # Saltamos este usuario, ya está registrado

                # Generar el username a partir del apellido y nombre
                base_username = (user_data.get("apellido") + "_" + user_data.get("nombre")).replace(" ", "_")

                # Verificar si ya existe un usuario con el mismo username
                username = base_username
                count = 1
                while Usuario.objects.filter(username=username).exists():
                    # Si el nombre de usuario ya existe, generar uno nuevo añadiendo un número
                    username = f"{base_username}_{count}"
                    count += 1

                # Buscar afiliado con el FPA proporcionado
                afiliados = Afiliado.objects.filter(fpa=user_data.get("fpa"))

                # Obtener uplink y link del afiliado si existe
                uplink = afiliados[0].uplink if afiliados.exists() else user_data.get("uplink")
                link = afiliados[0].url if afiliados.exists() else user_data.get("link")

                # Crear el nuevo usuario
                new_user = Usuario(
                    username=username,
                    fpa=user_data.get("fpa") or None,
                    idCliente=user_data.get("idCliente") or None,
                    email=user_data.get("email"),
                    first_name=user_data.get("nombre"),
                    last_name=user_data.get("apellido"),
                    telephone=user_data.get("telefono"),
                    wallet=user_data.get("wallet"),
                    uplink=uplink or "",
                    link=("https://livecommunity.info/Afiliado/" if link is None else link),
                    registrado=user_data.get("registrado", False),
                    aceptado=user_data.get("status", False),
                    userTelegram=user_data.get("userTelegram") or None,
                    password=user_data.get("password", "default_password"),
                )

                try:
                    # Guardar el usuario en la base de datos
                    new_user.save()

                    # Crear URLs si FPA no es None
                    if new_user.fpa:
                        try:
                            Url.objects.create(
                                name="Afiliado URL",
                                url=f"https://livecommunity.info/Afiliado/{new_user.fpa}",
                                usuario=new_user,
                                tipoUrl=TipoUrl.objects.get(id=1),
                            )
                            Url.objects.create(
                                name="Skilling Partners URL",
                                url=f"https://go.skillingpartners.com/visit/?bta=35881&nci=5846&utm_campaign={new_user.fpa}",
                                usuario=new_user,
                                tipoUrl=TipoUrl.objects.get(id=2),
                            )
                        except Exception as e:
                            print(f"Error creando URLs para {new_user.username}: {e}")

                    # Asignar roles al usuario
                    roles = user_data.get("roles", [])  # Lista de IDs de roles
                    for rol_id in roles:
                        try:
                            rol = Rol.objects.get(id=rol_id)
                            UsuarioRol.objects.create(usuario=new_user, rol=rol)
                        except Rol.DoesNotExist:
                            return JsonResponse(
                                {"message": f"Rol con ID {rol_id} no existe"}, status=400
                            )

                    # Asignar servicios al usuario (si existen en los datos)
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

            return JsonResponse({"message": "Usuarios creados exitosamente"}, status=200)

        else:
            return JsonResponse(
                {"message": "Error en la petición a la URL externa"},
                status=response.status_code,
            )

    except requests.exceptions.RequestException as e:
        return JsonResponse({"message": f"Error de conexión: {str(e)}"}, status=500)
    except json.JSONDecodeError:
        return JsonResponse({"message": "Error al decodificar el JSON"}, status=403)





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
