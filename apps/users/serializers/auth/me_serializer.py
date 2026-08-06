from rest_framework import serializers

from apps.users.dto import MeResult
from apps.users.serializers.user_serializer import UserDetailSerializer


class MeResponseSerializer(serializers.Serializer):
    """
    Serializer de respuesta del endpoint ``GET /auth/me``.

    Serializa únicamente la información del usuario autenticado.
    """

    user = UserDetailSerializer(read_only=True)

    def to_representation(self, instance: MeResult) -> dict:
        """Convierte un ``MeResult`` en la respuesta JSON del API."""

        return {
            "user": UserDetailSerializer(instance.user).data,
        }
