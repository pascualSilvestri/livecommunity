from django.urls import path
from . import views

app_name = 'cliente'


urlpatterns = [
      path('<str:idCliente>', views.cliente, name = 'cliente'),
]