from django.urls import path
from apps.api.skilling.views import afiliado, clienteform

app_name = 'registroPape'


urlpatterns = [
      path('<str:idAfiliado>', afiliado, name = 'afiliado'),
      path('clienteForm/', clienteform, name='clienteform'),
      # Ruta para enviar los datos en formato Json hacia JS
]