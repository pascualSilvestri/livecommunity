from rest_framework import serializers
from .models import (
    CPA,
    BonoCpa,
    BonoCpaIndirecto,
    Registros_ganancias,
    Registros_cpa,
    SpreadIndirecto,
    Cuenta,
    BonoAPagar,
    Spread
)

class CPASerializer(serializers.ModelSerializer):
    class Meta:
        model = CPA
        fields = '__all__'

class BonoCpaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonoCpa
        fields = '__all__'

class BonoCpaIndirectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonoCpaIndirecto
        fields = '__all__'

class RegistrosGananciasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registros_ganancias
        fields = '__all__'

class RegistrosCpaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registros_cpa
        fields = '__all__'

class SpreadIndirectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpreadIndirecto
        fields = '__all__'

class CuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuenta
        fields = '__all__'

class BonoAPagarSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonoAPagar
        fields = '__all__'

class SpreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spread
        fields = '__all__'