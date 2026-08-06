"""
Script para limpiar el campo deleted_at de registros que fueron
eliminados lógicamente pero que ya no deberían estar ocultos.
Ejecutar: python fix_deleted_at.py
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()

from apps.users.models import Role, User
from apps.users.models.user_role import UserRole

r = Role.all_objects.filter(deleted_at__isnull=False).update(deleted_at=None)
u = User.all_objects.filter(deleted_at__isnull=False).update(deleted_at=None)
ur = UserRole.all_objects.filter(deleted_at__isnull=False).update(deleted_at=None)

print(f"Roles limpiados: {r}")
print(f"Usuarios limpiados: {u}")
print(f"UserRoles limpiados: {ur}")
print("¡Listo! Puedes eliminar este archivo.")
