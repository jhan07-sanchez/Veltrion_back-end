from rest_framework import serializers

from apps.users.dto import SecurityContextResult


class SecurityContextResponseSerializer(serializers.Serializer):
    """
    Serializer de respuesta del endpoint ``GET /security/context``.

    Serializa únicamente roles, permisos efectivos y acciones.
    """

    roles = serializers.ListField(
        child=serializers.CharField(),
        read_only=True,
    )
    permissions = serializers.DictField(
        child=serializers.DictField(child=serializers.BooleanField()),
        read_only=True,
    )
    actions = serializers.DictField(
        child=serializers.DictField(child=serializers.BooleanField()),
        read_only=True,
    )

    def to_representation(self, instance: SecurityContextResult) -> dict:
        """Convierte un ``SecurityContextResult`` en contexto de autorización."""

        return {
            "roles": instance.roles,
            "permissions": instance.permissions,
            "actions": instance.actions,
        }
