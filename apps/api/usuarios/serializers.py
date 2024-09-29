from rest_framework import serializers
from .models import Usuario, OtroModelo

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class OtroModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtroModelo
        fields = '__all__'