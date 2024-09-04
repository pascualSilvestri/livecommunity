
import json
from django.http import JsonResponse

from apps.afiliado.models import Afiliado
from apps.usuarios.models import Rol, Servicio, Usuario, UsuarioRol, UsuarioServicio
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def postNewUser(request):
    if 'application/json' in request.content_type:
        try:
            # Decodificar el cuerpo de la solicitud como JSON
            data = json.loads(request.body)
            
            # Verificar si ya existe un usuario con el FPA proporcionado
            if Usuario.objects.filter(fpa=data.get('fpa')).exists():
                return JsonResponse({'message': 'Usuario ya registrado'}, status=401)

            # Buscar afiliado con el FPA proporcionado
            afiliados = Afiliado.objects.filter(fpa=data.get('fpa'))
            
            if afiliados.exists():
                uplink = afiliados[0].uplink
                link = afiliados[0].url

                # Crear el nuevo usuario
                new_user = Usuario(
                    username=(data.get('fpa') + "_" + data.get('first_name')).replace(' ', '_'),
                    fpa=data.get('fpa'),
                    email=data.get('email'),
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name'),
                    password=make_password(data.get('password')),  # Hashear la contraseña
                    telephone=data.get('telephone'),
                    wallet=data.get('wallet'),
                    uplink=uplink or '',
                    link=link or ''
                )
                new_user.registrado = True

                # Guardar el usuario en la base de datos
                new_user.save()

                # Asignar roles al usuario
                roles = data.get('roles', [])  # Lista de IDs de roles
                for rol_id in roles:
                    try:
                        rol = Rol.objects.get(id=rol_id)
                        UsuarioRol.objects.create(usuario=new_user, rol=rol)
                    except Rol.DoesNotExist:
                        return JsonResponse({'message': f'Rol con ID {rol_id} no existe'}, status=400)

                # Asignar servicios al usuario
                servicios = data.get('servicios', [])  # Lista de IDs de servicios
                for servicio_id in servicios:
                    try:
                        servicio = Servicio.objects.get(id=servicio_id)
                        UsuarioServicio.objects.create(usuario=new_user, servicio=servicio)
                    except Servicio.DoesNotExist:
                        return JsonResponse({'message': f'Servicio con ID {servicio_id} no existe'}, status=400)

                return JsonResponse({'message': 'Usuario creado exitosamente'}, status=200)

            else:
                return JsonResponse({'message': 'Usuario no habilitado para registrarse'}, status=402)
        
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Error al decodificar el JSON'}, status=403)
    
    else:
        return JsonResponse({'message': 'Tipo de contenido no válido'}, status=404)



@require_POST
def createUser(request):
    try:
        # Extraer los datos de la solicitud
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        fpa = request.POST.get('fpa')
        idCliente = request.POST.get('idCliente')
        telephone = request.POST.get('telephone')
        userTelegram = request.POST.get('userTelegram', 'none')
        registrado = request.POST.get('registrado', False)
        aceptado = request.POST.get('aceptado', False)
        fondeado = request.POST.get('fondeado', False)
        eliminado = request.POST.get('eliminado', False)

        # Recibir roles y servicios como listas de IDs (o nombres)
        roles = request.POST.getlist('roles')  # Lista de IDs o nombres de roles
        servicios = request.POST.getlist('servicios')  # Lista de IDs o nombres de servicios

        # Validar que se tengan los campos obligatorios
        if not username or not password or not email:
            return JsonResponse({'error': 'El nombre de usuario, contraseña y correo electrónico son obligatorios.'}, status=400)

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
            eliminado=eliminado
        )

        # Asignar roles si existen
        if roles:
            for rol_id in roles:
                try:
                    rol = Rol.objects.get(id=rol_id)  # Buscar el rol por ID
                    UsuarioRol.objects.create(usuario=new_user, rol=rol)  # Relación ManyToMany
                except Rol.DoesNotExist:
                    return JsonResponse({'error': f'El rol con id {rol_id} no existe.'}, status=400)

        # Asignar servicios si existen
        if servicios:
            for servicio_id in servicios:
                try:
                    servicio = Servicio.objects.get(id=servicio_id)  # Buscar el servicio por ID
                    UsuarioServicio.objects.create(usuario=new_user, servicio=servicio)  # Relación ManyToMany
                except Servicio.DoesNotExist:
                    return JsonResponse({'error': f'El servicio con id {servicio_id} no existe.'}, status=400)

        # Guardar el usuario en la base de datos
        new_user.save()

        # Retornar una respuesta exitosa
        return JsonResponse({'message': 'Usuario creado exitosamente', 'usuario': new_user.username})

    except Exception as e:
        # En caso de error, retornar un mensaje de error
        return JsonResponse({'error': str(e)}, status=500)



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

        rolesAndUsuario.append({
            'username': usuario.username,
            'roles': roles,
            'servicios':servicios
        })

    
    return JsonResponse({'users': rolesAndUsuario})