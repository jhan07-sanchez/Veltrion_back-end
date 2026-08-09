from rest_framework import serializers

from apps.users.models import UserRole


class UserRoleListSerializer(serializers.ModelSerializer):
    """
    Serializer para listar las asignaciones de roles.
    """

    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    role_name = serializers.CharField(
        source="role.role_name",
        read_only=True,
    )
    assigned_at = serializers.DateTimeField(
        source="created_at",
        read_only=True,
    )

    class Meta:
        model = UserRole

        fields = (
            "id_user_role",
            "username",
            "role_name",
            "assigned_at",
        )

        read_only_fields = fields


class UserRoleDetailSerializer(serializers.ModelSerializer):
    """
    Serializer para visualizar el detalle
    de una asignacion.
    """

    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    role_name = serializers.CharField(
        source="role.role_name",
        read_only=True,
    )

    class Meta:
        model = UserRole

        fields = (
            "id_user_role",
            "user",
            "username",
            "role",
            "role_name",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id_user_role",
            "created_at",
            "updated_at",
        )


class UserRoleCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear asignaciones de roles.
    """

    class Meta:
        model = UserRole

        fields = (
            "user",
            "role",
        )


class UserRoleUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para actualizar
    asignaciones de roles.
    """

    class Meta:
        model = UserRole

        fields = (
            "user",
            "role",
        )
