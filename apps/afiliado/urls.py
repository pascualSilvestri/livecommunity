from django.urls import path
from . import views

app_name = 'afiliado'


urlpatterns = [
      path('<str:idAfiliado>', views.afiliado, name = 'afiliado'),
]