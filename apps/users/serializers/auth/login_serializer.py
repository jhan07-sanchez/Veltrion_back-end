from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.users.dto import LoginResult
from apps.users.serializers.user_serializer import UserDetailSerializer

User = get_user_model()


class AuthLoginSerializer(serializers.Serializer):
    """Serializer para validar las credenciales de inicio de sesión."""

    username = serializers.CharField(
        max_length=150,
        required=True,
        trim_whitespace=True,
        help_text="Nombre de usuario.",
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        trim_whitespace=False,
        style={"input_type": "password"},
        help_text="Contraseña del usuario.",
    )

    def validate_username(self, value: str) -> str:
        """Normaliza el nombre de usuario."""

        return value.strip().lower()

    def validate(self, attrs: dict) -> dict:
        """Valida que las credenciales hayan sido enviadas."""

        username = attrs.get("username")
        password = attrs.get("password")

        if not username:
            raise serializers.ValidationError(
                {"username": "El nombre de usuario es obligatorio."},
            )

        if not password:
            raise serializers.ValidationError(
                {"password": "La contraseña es obligatoria."},
            )

        return attrs


class LoginResponseSerializer(serializers.Serializer):
    """
    Serializer de respuesta del login.

    Serializa únicamente usuario y tokens JWT.
    """

    user = UserDetailSerializer(read_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    def to_representation(self, instance: LoginResult) -> dict:
        """Convierte un ``LoginResult`` en la respuesta JSON del API."""

        return {
            "user": UserDetailSerializer(instance.user).data,
            "access_token": instance.access_token,
            "refresh_token": instance.refresh_token,
        }
