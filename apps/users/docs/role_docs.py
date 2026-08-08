from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)

from apps.core.docs.api_response_schema import build_api_response_schema
from apps.core.docs.error_schemas import (
    ApiErrorResponseSerializer,
    ValidationErrorResponseSerializer,
)
from apps.users.serializers.role_serializer import (
    RoleCreateSerializer,
    RoleDetailSerializer,
    RoleListSerializer,
    RoleUpdateSerializer,
)

role_list_schema = extend_schema(
    tags=["Roles"],
    summary="Listar roles",
    description=("Obtiene el listado de todos los roles registrados en el sistema."),
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="RoleListResponse",
                data_serializer=RoleListSerializer,
                is_list=True,
            ),
            description="Listado de roles.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="No autenticado."
        ),
        403: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Permisos denegados."
        ),
    },
)

role_detail_schema = extend_schema(
    tags=["Roles"],
    summary="Obtener rol",
    description="Obtiene la información detallada de un rol.",
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="RoleDetailResponse",
                data_serializer=RoleDetailSerializer,
            ),
            description="Información del rol.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="No autenticado."
        ),
        403: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Permisos denegados."
        ),
        404: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Rol no encontrado."
        ),
    },
)

role_create_schema = extend_schema(
    tags=["Roles"],
    summary="Crear rol",
    description="Crea un nuevo rol dentro del sistema.",
    request=RoleCreateSerializer,
    responses={
        201: OpenApiResponse(
            response=build_api_response_schema(
                name="RoleCreateResponse",
                data_serializer=RoleDetailSerializer,
            ),
            description="Rol creado correctamente.",
        ),
        400: OpenApiResponse(
            response=ValidationErrorResponseSerializer,
            description="Datos inválidos de validación.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="No autenticado."
        ),
        403: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Permisos denegados."
        ),
    },
    examples=[
        OpenApiExample(
            name="Crear Rol",
            request_only=True,
            value={
                "role_name": "Administrador",
                "role_description": "Control total del sistema",
                "is_active": True,
            },
        )
    ],
)

role_update_schema = extend_schema(
    tags=["Roles"],
    summary="Actualizar rol",
    description="Actualiza completamente un rol.",
    request=RoleUpdateSerializer,
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="RoleUpdateResponse",
                data_serializer=RoleDetailSerializer,
            ),
            description="Rol actualizado correctamente.",
        ),
        400: OpenApiResponse(
            response=ValidationErrorResponseSerializer, description="Datos inválidos."
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="No autenticado."
        ),
        403: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Permisos denegados."
        ),
        404: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Rol no encontrado."
        ),
    },
)

role_partial_update_schema = extend_schema(
    tags=["Roles"],
    summary="Actualizar parcialmente un rol",
    description="Actualiza uno o varios campos de un rol.",
    request=RoleUpdateSerializer,
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="RolePartialUpdateResponse",
                data_serializer=RoleDetailSerializer,
            ),
            description="Rol actualizado correctamente.",
        ),
        400: OpenApiResponse(
            response=ValidationErrorResponseSerializer, description="Datos inválidos."
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="No autenticado."
        ),
        403: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Permisos denegados."
        ),
        404: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Rol no encontrado."
        ),
    },
)

role_delete_schema = extend_schema(
    tags=["Roles"],
    summary="Desactivar rol",
    description="Realiza el borrado lógico del rol.",
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="RoleDeleteResponse",
            ),
            description="Rol desactivado correctamente.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="No autenticado."
        ),
        403: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Permisos denegados."
        ),
        404: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Rol no encontrado."
        ),
    },
)

role_restore_schema = extend_schema(
    tags=["Roles"],
    summary="Restaurar rol",
    description="Reactiva un rol previamente desactivado.",
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="RoleRestoreResponse",
                data_serializer=RoleDetailSerializer,
            ),
            description="Rol restaurado correctamente.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="No autenticado."
        ),
        403: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Permisos denegados."
        ),
        404: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Rol no encontrado."
        ),
    },
)
