from rest_framework.permissions import BasePermission

from apps.users.models import UserRole


class BaseRolePermission(BasePermission):
    """
    Clase base para validar permisos dinámicos
    definidos en el modelo Role.
    """

    required_permission: str | None = None

    def has_permission(self, request, view) -> bool:
        """
        Verifica si el usuario autenticado posee
        el permiso requerido.
        """

        if not request.user.is_authenticated:
            return False

        if self.required_permission is None:
            return False

        return UserRole.objects.filter(
            user=request.user,
            is_active=True,
            role__is_active=True,
            **{f"role__{self.required_permission}": True},
        ).exists()
