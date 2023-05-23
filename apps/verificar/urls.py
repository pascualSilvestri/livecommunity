from django.urls import path
from . import views

app_name = 'verificar'


urlpatterns = [
      path('', views.verificar, name='verificar'),
]