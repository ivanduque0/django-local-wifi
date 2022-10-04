from rest_framework import serializers 
from .models import apertura

class aperturaserializer(serializers.ModelSerializer):
    cedula = serializers.CharField()
    id_usuario = serializers.CharField()