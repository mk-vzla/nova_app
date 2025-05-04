from rest_framework import serializers
from .models_copy import CopiaJuego  # Importa desde models_copy

class CopiaJuegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CopiaJuego
        fields = '__all__'