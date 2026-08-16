from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)

from apps.core.docs.api_response_schema import build_api_response_schema
from apps.core.docs.error_schemas import (
    ApiErrorResponseSerializer,
    ValidationErrorResponseSerializer,
)
from apps.customers.serializers.customer_serializer import (
    CustomerCreateSerializer,
    CustomerDetailSerializer,
    CustomerListSerializer,
    CustomerUpdateSerializer,
)

pagination_parameters = [
    OpenApiParameter(
        name="page",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.QUERY,
        description="Número de página para la paginación.",
        required=False,
    ),
    OpenApiParameter(
        name="page_size",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.QUERY,
        description="Cantidad de resultados por página.",
        required=False,
    ),
]

customer_list_schema = extend_schema(
    tags=["Customers"],
    summary="Listar clientes",
    description="Obtiene el listado paginado de clientes registrados en el sistema.",
    parameters=pagination_parameters,
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="CustomerListApiResponse",
                data_serializer=CustomerListSerializer,
                is_list=True,
            ),
            description="Clientes obtenidos correctamente.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="Token inválido, expirado o usuario no autenticado.",
        ),
        403: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="El usuario no tiene permiso para consultar clientes.",
        ),
    },
)

customer_detail_schema = extend_schema(
    tags=["Customers"],
    summary="Obtener cliente",
    description="Obtiene la información detallada de un cliente mediante su identificador.",
    parameters=[
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="Identificador único del cliente.",
            required=True,
        )
    ],
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="CustomerDetailApiResponse",
                data_serializer=CustomerDetailSerializer,
            ),
            description="Cliente obtenido correctamente.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="Token inválido, expirado o usuario no autenticado.",
        ),
        403: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="El usuario no tiene permiso para consultar clientes.",
        ),
        404: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="Cliente no encontrado.",
        ),
    },
)

customer_create_schema = extend_schema(
    tags=["Customers"],
    summary="Crear cliente",
    description=(
        "Registra un nuevo cliente en el sistema. "
        "El número de documento debe ser único."
    ),
    request=CustomerCreateSerializer,
    responses={
        201: OpenApiResponse(
            response=build_api_response_schema(
                name="CustomerCreateApiResponse",
                data_serializer=CustomerDetailSerializer,
            ),
            description="Cliente creado correctamente.",
        ),
        400: OpenApiResponse(
            response=ValidationErrorResponseSerializer,
            description="Los datos enviados no son válidos. Códigos posibles: CUSTOMER_ALREADY_EXISTS.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="Token inválido, expirado o usuario no autenticado.",
        ),
        403: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="El usuario no tiene permiso para crear clientes.",
        ),
    },
    examples=[
        OpenApiExample(
            "Crear Cliente",
            request_only=True,
            value={
                "document_type": "CC",
                "document_number": "123456789",
                "first_name": "Juan",
                "last_name": "Pérez",
                "email": "juan@example.com",
                "phone_number": "3001234567",
                "is_active": True
            },
        )
    ],
)

customer_update_schema = extend_schema(
    tags=["Customers"],
    summary="Actualizar cliente",
    description="Actualiza completamente la información de un cliente existente.",
    parameters=[
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="Identificador único del cliente a actualizar.",
            required=True,
        )
    ],
    request=CustomerUpdateSerializer,
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="CustomerUpdateApiResponse",
                data_serializer=CustomerDetailSerializer,
            ),
            description="Cliente actualizado correctamente.",
        ),
        400: OpenApiResponse(
            response=ValidationErrorResponseSerializer,
            description="Los datos enviados no son válidos. Códigos posibles: CUSTOMER_ALREADY_EXISTS.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="Token inválido, expirado o usuario no autenticado.",
        ),
        403: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="El usuario no tiene permiso para actualizar clientes.",
        ),
        404: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="Cliente no encontrado.",
        ),
    },
)

customer_partial_update_schema = extend_schema(
    tags=["Customers"],
    summary="Actualizar parcialmente cliente",
    description="Actualiza parcialmente la información de un cliente existente.",
    parameters=[
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="Identificador único del cliente a actualizar parcialmente.",
            required=True,
        )
    ],
    request=CustomerUpdateSerializer,
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="CustomerPartialUpdateApiResponse",
                data_serializer=CustomerDetailSerializer,
            ),
            description="Cliente actualizado correctamente.",
        ),
        400: OpenApiResponse(
            response=ValidationErrorResponseSerializer,
            description="Los datos enviados no son válidos. Códigos posibles: CUSTOMER_ALREADY_EXISTS.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="Token inválido, expirado o usuario no autenticado.",
        ),
        403: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="El usuario no tiene permiso para actualizar clientes.",
        ),
        404: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="Cliente no encontrado.",
        ),
    },
)

customer_delete_schema = extend_schema(
    tags=["Customers"],
    summary="Desactivar cliente",
    description=(
        "Desactiva lógicamente un cliente. "
        "El registro no se elimina físicamente de la base de datos."
    ),
    parameters=[
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="Identificador único del cliente a desactivar.",
            required=True,
        )
    ],
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="CustomerDeleteApiResponse",
            ),
            description="Cliente desactivado correctamente.",
        ),
        400: OpenApiResponse(
            response=ValidationErrorResponseSerializer,
            description="No fue posible desactivar el cliente. Códigos posibles: CUSTOMER_INACTIVE.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="Token inválido, expirado o usuario no autenticado.",
        ),
        403: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="El usuario no tiene permiso para eliminar clientes.",
        ),
        404: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="Cliente no encontrado.",
        ),
    },
)

customer_restore_schema = extend_schema(
    tags=["Customers"],
    summary="Restaurar cliente",
    description="Reactiva un cliente previamente desactivado.",
    parameters=[
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="Identificador único del cliente a restaurar.",
            required=True,
        )
    ],
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="CustomerRestoreApiResponse",
                data_serializer=CustomerDetailSerializer,
            ),
            description="Cliente restaurado correctamente.",
        ),
        400: OpenApiResponse(
            response=ValidationErrorResponseSerializer,
            description="No fue posible restaurar el cliente.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="Token inválido, expirado o usuario no autenticado.",
        ),
        403: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="El usuario no tiene permiso para restaurar clientes.",
        ),
        404: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="Cliente no encontrado.",
        ),
    },
)
