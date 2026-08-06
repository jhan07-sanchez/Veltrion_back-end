from rest_framework import serializers


class AuthRefreshSerializer(serializers.Serializer):
    """
    Serializer encargado de validar el Refresh Token recibido
    para generar un nuevo Access Token.
    """

    refresh = serializers.CharField(
        required=True,
        help_text="Refresh Token del usuario.",
    )
