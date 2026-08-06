from rest_framework import serializers


class AuthLogoutSerializer(serializers.Serializer):
    """
    Serializer para el cierre de sesión.

    Valida que se proporcione el Refresh Token para invalidarlo.
    """

    refresh = serializers.CharField(
        required=True,
        error_messages={
            "required": "El campo refresh es obligatorio.",
            "blank": "El campo refresh no puede estar en blanco.",
        },
    )
