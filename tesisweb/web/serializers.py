from rest_framework import serializers 

class aperturaserializer(serializers.Serializer):
    acceso = serializers.CharField()
    id_usuario = serializers.CharField()