from rest_framework import serializers


class AuthRefreshResponseSerializer(serializers.Serializer):
    """
    Serializer utilizado para documentar la respuesta
    del endpoint de renovación de tokens.
    """

    access = serializers.CharField(help_text="Nuevo Access Token.")
