from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


from apps.users.models import User
from .role_serializer import RoleListSerializer


# serializer para listar usuarios
class UserListSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User

        fields = (
            "id_user",
            "username",
            "first_name",
            "last_name",
            "email",
            "document_number",
            "roles",
            "is_active",
        )

    def get_roles(self, obj):
        """
        Retorna todos los roles asignados al usuario.
        """

        roles = [ur.role for ur in obj.user_roles.all() if ur.role.is_active]

        return RoleListSerializer(
            roles,
            many=True,
        ).data

class UserDetailSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User

        fields = (
            "id_user",
            "username",
            "first_name",
            "last_name",
            "email",
            "document_number",
            "phone_number",
            "roles",
            "is_active",
            "created_at",
            "updated_at",
        )

    def get_roles(self, obj):
        roles = [ur.role for ur in obj.user_roles.all() if ur.role.is_active]

        return RoleListSerializer(
            roles,
            many=True,
        ).data


#Serializer para crear usuarios
class UserCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password],)

    class Meta:
        model = User

        fields = (
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "document_number",
            "phone_number",
        )

        extra_kwargs = {
            "username": {"validators": []},
            "email": {"validators": []},
            "document_number": {"validators": []},
        }



#Serializer para actualizar usuarios
class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "is_active",
        )

        extra_kwargs = {
            "username": {"validators": []},
            "email": {"validators": []},
            "document_number": {"validators": []},
        }
