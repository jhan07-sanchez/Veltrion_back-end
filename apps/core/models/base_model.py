from django.db import models
from django.utils import timezone


class BaseManager(models.Manager):
    """
    Manager base que filtra los registros eliminados lógicamente.
    """

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class BaseModel(models.Model):
    """
    Modelo base para todas las entidades del sistema.

    Contiene únicamente los campos comunes que serán
    heredados por los demás modelos. Incluye Soft Delete.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización",
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de eliminación",
    )

    objects = BaseManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """
        Sobrescribe el método delete para realizar un borrado lógico (Soft Delete).
        """
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def restore(self):
        """
        Restaura un registro eliminado lógicamente.
        """
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])
