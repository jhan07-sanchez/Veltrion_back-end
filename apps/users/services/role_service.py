from django.db import transaction

from apps.core.exceptions.custom_exceptions import (
    RoleAlreadyExistsException,
    RoleInactiveException,
)
from apps.core.services.base_service import BaseService
from apps.users.models import Role


class RoleService(BaseService[Role]):
    """
    Servicio encargado de la lógica de negocio relacionada con los roles.
    """

    def __init__(self):
        super().__init__(Role)

    def validate(self, data: dict, instance=None) -> dict:
        role_name = data.get("role_name")
        if instance is None:
            if role_name and Role.objects.filter(role_name__iexact=role_name).exists():
                raise RoleAlreadyExistsException()
        else:
            if (
                role_name
                and Role.objects.filter(role_name__iexact=role_name)
                .exclude(pk=instance.pk)
                .exists()
            ):
                raise RoleAlreadyExistsException()
        return data

    def perform_create(self, data: dict) -> Role:
        role = Role(**data)
        role.full_clean()
        role.save()
        return role

    def perform_update(self, instance: Role, data: dict) -> Role:
        for field, value in data.items():
            setattr(instance, field, value)
        instance.full_clean()
        instance.save()
        return instance

    def perform_delete(self, instance: Role, soft_delete: bool = True) -> None:
        if not instance.is_active:
            raise RoleInactiveException()
        instance.is_active = False
        instance.full_clean()
        instance.save(update_fields=["is_active", "updated_at"])
        if soft_delete:
            instance.delete()

    @staticmethod
    @transaction.atomic
    def create_role(validated_data: dict) -> Role:
        """
        Crea un nuevo rol aplicando las reglas de negocio.
        """
        return RoleService().create(**validated_data)

    @staticmethod
    @transaction.atomic
    def update_role(
        role: Role,
        validated_data: dict,
    ) -> Role:
        """
        Actualiza un rol aplicando las reglas de negocio.
        """
        return RoleService().update(role, **validated_data)

    @staticmethod
    @transaction.atomic
    def deactivate_role(role: Role) -> Role:
        """
        Realiza el borrado lógico de un rol.

        No elimina el registro físicamente de la base de datos.
        """
        RoleService().delete(role, soft_delete=False)
        return role

    @staticmethod
    @transaction.atomic
    def restore_role(role: Role) -> Role:
        """
        Reactiva un rol previamente desactivado.
        """
        role.is_active = True
        role.save(update_fields=["is_active", "updated_at"])
        role.restore()
        return role
