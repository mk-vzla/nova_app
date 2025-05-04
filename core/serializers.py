from rest_framework import serializers
from .models_copy import CopiaJuego, AliasSugerido  # Importa desde models_copy

class CopiaJuegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CopiaJuego
        fields = '__all__'



class AliasSugeridoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AliasSugerido
        fields = '__all__'

    def validate_alias(self, value):
        """
        Valida que el alias no contenga palabras prohibidas.
        """
        if any(palabra in value.lower() for palabra in PALABRAS_PROHIBIDAS):
            raise serializers.ValidationError("El alias contiene palabras prohibidas.")
        return value
    























































PALABRAS_PROHIBIDAS = [
    "password",
    "123456",
    "sexo",
    "violencia",
    "droga",
    "asesino",
    "hacker",
    "pirata",
    "fraude",
    "racismo",
    "odio",
    "terror",
    "bomba",
    "crimen",
    "ilegal",
    "prohibido",
    "malware",
    "phishing",
    "spam",
    "virus",
    "troll",
    "insulto",
    "ofensivo",
    "abusivo",
    "estafa",
    "pornografía",
    "nazi",
    "homofobia",
    "xenofobia",
    "pedofilia",
    "violador",
    "asesinato",
    "suicidio",
    "armas",
    "corrupción",
    "chantaje",
    "extorsión",
    "hack",
    "crack",
    "falsificación",
    "engaño",
    "mentira",
    "ilegalidad",
    "contrabando",
    "terrorismo",
    "radical",
    "racial",
    "discriminación",
    "prostitución",
    "mafioso",
    "delincuente",
    "viola"
  ]