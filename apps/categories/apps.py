from django.apps import AppConfig


class CategoriesConfig(AppConfig):
    """
    Configuración para la aplicación de Categorias.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.categories"
    verbose_name = "Categorias"
