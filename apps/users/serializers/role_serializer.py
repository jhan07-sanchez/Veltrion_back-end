from rest_framework import serializers

from apps.core.security.registry import SecurityRegistry
from apps.users.models import Role
from apps.users.services.role_service import RoleService


class RolePermissionsField(serializers.DictField):
    """
    Campo especializado para validar los permisos dinámicos
    contra SecurityRegistry.
    """

    child = serializers.BooleanField()

    def to_internal_value(self, data):
        """
        Valida que los códigos recibidos existan en el catálogo
        central de seguridad.
        """

        data = super().to_internal_value(data)

        valid_codes = set(SecurityRegistry.get_all_security_codes())

        invalid_codes = [code for code in data if code not in valid_codes]

        if invalid_codes:
            raise serializers.ValidationError(
                {
                    "invalid_permissions": (
                        "Los siguientes códigos de seguridad no existen en el catálogo."
                    ),
                    "codes": invalid_codes,
                }
            )

        return data


class RoleListSerializer(serializers.ModelSerializer):
    """
    Serializer para listar los roles del sistema.
    """

    class Meta:
        model = Role

        fields = (
            "id_role",
            "role_name",
            "role_description",
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
            "permissions",
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

    permissions = RolePermissionsField(
        required=False,
        default=dict,
    )

    class Meta:
        model = Role

        fields = (
            "role_name",
            "role_description",
            "permissions",
            "is_active",
        )

    def create(self, validated_data):
        """
        Delega la creación del rol al servicio de dominio.
        """

        return RoleService.create_role(validated_data)


class RoleUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer utilizado para actualizar un rol existente.
    """

    permissions = RolePermissionsField(
        required=False,
    )

    class Meta:
        model = Role

        fields = (
            "role_name",
            "role_description",
            "permissions",
            "is_active",
        )

    def update(self, instance, validated_data):
        """
        Delega la actualización del rol al servicio de dominio.
        """

        return RoleService.update_role(
            role=instance,
            validated_data=validated_data,
        )
