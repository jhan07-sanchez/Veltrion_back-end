from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"
    verbose_name = "Usuarios"

    def ready(self) -> None:
        """
        Registra los grupos, módulos y permisos de la aplicación Users
        en el SecurityRegistry al iniciar Django.
        """

        from apps.core.security import SecurityRegistry
        from apps.core.security.security_data import SECURITY_GROUPS, SECURITY_MODULES

        # ==================================================================
        # REGISTRO DE GRUPOS CONTENEDORES
        # ==================================================================
        for group in SECURITY_GROUPS:
            SecurityRegistry.register_group(**group)

        # ==================================================================
        # REGISTRO DE MÓDULOS
        # ==================================================================
        for module in SECURITY_MODULES:
            SecurityRegistry.register_module(**module)
