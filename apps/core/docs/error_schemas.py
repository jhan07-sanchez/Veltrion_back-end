from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import serializers

from apps.core.docs.api_response_schema import BaseApiResponseSerializer


class ApiErrorResponseSerializer(BaseApiResponseSerializer):
    """
    Esquema estándar para respuestas de error de la API.
    """
    success = serializers.BooleanField(default=False, help_text="Siempre es false en caso de error.")
    code = serializers.CharField(
        default="ERROR", help_text="Código del error (ej. NOT_FOUND, PERMISSION_DENIED)."
    )
    message = serializers.CharField(
        default="Ha ocurrido un error.", help_text="Mensaje descriptivo del error."
    )
    data = serializers.DictField(default=None, allow_null=True)
    errors = serializers.DictField(
        default=None, allow_null=True, help_text="Detalle técnico adicional si está disponible."
    )


class ValidationErrorResponseSerializer(ApiErrorResponseSerializer):
    """
    Esquema estándar para errores de validación.
    """
    code = serializers.CharField(default="VALIDATION_ERROR")
    message = serializers.CharField(default="Error de validación.")
    errors = serializers.DictField(
        help_text="Diccionario donde la llave es el campo y el valor la lista de errores."
    )


def standard_error_responses(responses=None):
    """
    Decorador reutilizable para inyectar las respuestas de error estándar.
    
    Args:
        responses (list): Lista de códigos de error HTTP (ej: [400, 401, 403, 404, 500]).
    """
    if responses is None:
        responses = [400, 401, 403, 404, 500]

    mapping = {
        400: OpenApiResponse(
            response=ValidationErrorResponseSerializer,
            description="Error de validación o solicitud incorrecta.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="Autenticación fallida o token inválido.",
        ),
        403: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="Permisos insuficientes para realizar esta acción.",
        ),
        404: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="Recurso no encontrado.",
        ),
        500: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="Error interno del servidor.",
        ),
    }

    schema_responses = {code: mapping[code] for code in responses if code in mapping}

    return extend_schema(responses=schema_responses)
