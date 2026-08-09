from rest_framework import serializers


class PermissionCatalogItemSerializer(serializers.Serializer):
    """
    Representa un permiso o acción disponible en el sistema.
    """

    code = serializers.CharField()
    description = serializers.CharField()


class PermissionCatalogModuleSerializer(serializers.Serializer):
    """
    Representa un módulo del catálogo de seguridad.
    """

    module_id = serializers.CharField()
    label = serializers.CharField()
    icon = serializers.CharField(
        allow_blank=True,
    )
    parent = serializers.CharField(
        allow_null=True,
        required=False,
    )
    permissions = PermissionCatalogItemSerializer(
        many=True,
    )
    actions = PermissionCatalogItemSerializer(
        many=True,
    )


class PermissionCatalogResponseSerializer(serializers.Serializer):
    """
    Respuesta del catálogo dinámico de seguridad.
    """

    modules = PermissionCatalogModuleSerializer(
        many=True,
    )
