from django.urls import path
from apps.api.skilling.views import afiliado


app_name = 'registroPape'


urlpatterns = [
      path('<str:idAfiliado>', afiliado, name = 'afiliado'),   # Ruta para enviar los datos en formato Json hacia JS
]