"""
Servicio de dominio para construir el catalogo
dinamico de permisos y acciones de Veltrion.
"""
from __future__ import annotations

from apps.core.security.registry import SecurityRegistry




class PermissionCatalogService:
    """
    Servicio para consultar el catálogo dinámico de seguridad.
    """

    @staticmethod
    def get_catalog() -> dict[str, list[dict]]:
        """
        Obtiene el catálogo registrado en SecurityRegistry.
        """

        return {
            "modules": SecurityRegistry.get_permission_catalog(),
        }
