from apps.core.permissions.base_permission import BaseRolePermission


class HasUsersReadPermission(BaseRolePermission):
    """
    Permite listar usuarios.
    """

    required_permission = "users_read"


class HasUsersCreatePermission(BaseRolePermission):
    """
    Permite crear usuarios.
    """

    required_permission = "users_create"


class HasUsersUpdatePermission(BaseRolePermission):
    """
    Permite actualizar usuarios.
    """

    required_permission = "users_update"


class HasUsersDeletePermission(BaseRolePermission):
    """
    Permite eliminar usuarios.
    """

    required_permission = "users_delete"
