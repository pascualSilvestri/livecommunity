
import json
from django.http import JsonResponse

from apps.afiliado.models import Afiliado
from apps.usuarios.models import Usuario
from django.views.decorators.csrf import csrf_exempt


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




def users(request):
    
    return JsonResponse({
'users':'funciono'})