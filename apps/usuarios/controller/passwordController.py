import random
import json
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from ..models import Usuario, TokenPassword
from django.views.decorators.csrf import csrf_exempt

def generar_token():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

@csrf_exempt
def enviar_token_recuperacion(request):
    if request.method == 'POST':
        try:
            # Intentar decodificar el cuerpo JSON de la solicitud
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')

            if not email:
                return JsonResponse({'error': 'Email no proporcionado'}, status=400)

            print(f"Email recibido: {email}")  # Para depuración

            usuario = Usuario.objects.get(email=email)
            token = generar_token()
            
            # Calcular la fecha de expiración (5 minutos desde ahora)
            fecha_expiracion = timezone.now() + timedelta(minutes=5)
            
            # Guardar el token en el modelo
            TokenPassword.objects.create(
                usuario=usuario,
                token=token,
                fecha_expiracion=fecha_expiracion
            )
            
            # Enviar el token por correo
            asunto = 'Token de recuperación de contraseña'
            mensaje = f'Tu token de recuperación es: {token}\nEste token expirará en 5 minutos.'
            email_from = settings.EMAIL_HOST_USER
            destinatario = [email]
            
            try:
                send_mail(asunto, mensaje, email_from, destinatario, fail_silently=False)
                return JsonResponse({'mensaje': 'Token enviado con éxito'}, status=200)
            except Exception as e:
                return JsonResponse({'error': f'Error al enviar el correo: {str(e)}'}, status=500)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato de solicitud inválido'}, status=400)
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Error inesperado: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def validar_token(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            token = data.get('token')

            if not token:
                return JsonResponse({'error': 'Token no proporcionado'}, status=400)

            # Buscar el token en la base de datos
            token_obj = TokenPassword.objects.filter(token=token).first()

            if not token_obj:
                return JsonResponse({'error': 'Token inválido'}, status=400)

            # Verificar si el token ha expirado
            if token_obj.fecha_expiracion < timezone.now():
                return JsonResponse({'error': 'Token expirado'}, status=400)

            # Token válido, retornar información del usuario
            usuario = token_obj.usuario
            return JsonResponse({
                'mensaje': 'Token válido',
                'usuario': {
                    'fpa': usuario.fpa,
                    'email': usuario.email,
                }
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato de solicitud inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error inesperado: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


