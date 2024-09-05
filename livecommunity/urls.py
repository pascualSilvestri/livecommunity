"""
URL configuration for livecommunity project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name = 'home'),
    path('broker/skilling/',views.broker_skilling, name = 'broker_skilling'),
    path('presenciales/',views.presenciales, name = 'presenciales'),
    path('presenciales/consulta/',views.consultaForm, name = 'consultaForm'),
    path('servicios/',views.servicios, name = 'servicios'),
    path('Afiliado/',include('apps.registroPage.urls')),
    path('api/skilling/',include('apps.api.skilling.urls')),
    path('user/',include('apps.usuarios.urls')),
    path('<pk>',views.home_pk, name = 'home_pk'),
    #path('broker/<pk>',views.broker_pk, name = 'broker_pk'),
    path('broker/skilling/<pk>',views.broker_pk, name = 'broker_skilling_pk'),
    path('presenciales/<pk>',views.presenciales_pk, name = 'presenciales_pk'),
    path('servicios/<pk>',views.servicios_pk, name = 'servicios_pk'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
