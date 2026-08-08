from rest_framework import serializers

# Cache global para evitar duplicidad de esquemas con el mismo nombre
_response_schema_cache = {}


class BaseApiResponseSerializer(serializers.Serializer):
    """
    Clase base para construir la estructura de respuesta estándar.
    """

    success = serializers.BooleanField(
        default=True, help_text="Indica si la operación fue exitosa."
    )
    code = serializers.CharField(
        default="SUCCESS", help_text="Código interno del resultado de la operación."
    )
    message = serializers.CharField(
        default="Operación exitosa.", help_text="Mensaje descriptivo del resultado."
    )
    errors = serializers.DictField(
        allow_null=True,
        required=False,
        default=None,
        help_text="Detalle de errores si success es false.",
    )


def build_api_response_schema(
    name: str,
    data_serializer=None,
    is_list: bool = False,
    description: str = "Respuesta estandarizada de la API.",
):
    """
    Genera un Serializer dinámico y reutilizable para DRF Spectacular
    que envuelve cualquier serializer dentro del formato estandarizado ApiResponse.

    Elimina el uso de inline_serializer para evitar 'Anonymous Objects'
    y permite que el esquema se registre limpiamente en components/schemas/.
    """

    if name in _response_schema_cache:
        return _response_schema_cache[name]

    if data_serializer is None:
        data_field = serializers.DictField(
            allow_null=True, help_text="Datos dinámicos de la respuesta."
        )
    elif is_list:
        data_field = data_serializer(many=True, help_text="Lista de resultados.")
    else:
        data_field = data_serializer(help_text="Objeto de resultado.")

    # Usamos type() para generar una clase hija de BaseApiResponseSerializer
    schema_class = type(
        name, (BaseApiResponseSerializer,), {"data": data_field, "__doc__": description}
    )

    _response_schema_cache[name] = schema_class
    return schema_class
