from rest_framework import serializers

from apps.users.models import Role
from apps.users.services.role_service import RoleService


class RoleListSerializer(serializers.ModelSerializer):
    """
    Serializer para listar los roles del sistema.
    """

    class Meta:
        model = Role
        fields = (
            "id_role",
            "role_name",
            "is_active",
        )

        read_only_fields = fields


class RoleDetailSerializer(serializers.ModelSerializer):
    """
    Serializer para visualizar el detalle completo de un rol.
    """

    class Meta:
        model = Role

        fields = (
            "id_role",
            "role_name",
            "role_description",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id_role",
            "created_at",
            "updated_at",
        )


class RoleCreateSerializer(serializers.ModelSerializer):
    """
    Serializer utilizado para crear un nuevo rol.
    """

    class Meta:
        model = Role

        exclude = (
            "id_role",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        """
        Delega la creación al RoleService.
        """

        return RoleService.create_role(validated_data)


class RoleUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer utilizado para actualizar un rol existente.
    """

    class Meta:
        model = Role

        exclude = (
            "id_role",
            "created_at",
            "updated_at",
        )

    def update(self, instance, validated_data):
        """
        Delega la actualización al RoleService.
        """

        return RoleService.update_role(
            role=instance,
            validated_data=validated_data,
        )
