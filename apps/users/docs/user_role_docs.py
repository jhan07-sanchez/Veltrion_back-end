from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)

from apps.core.docs.api_response_schema import build_api_response_schema
from apps.core.docs.error_schemas import (
    ApiErrorResponseSerializer,
    ValidationErrorResponseSerializer,
)
from apps.users.serializers.user_role_serializer import (
    UserRoleCreateSerializer,
    UserRoleDetailSerializer,
    UserRoleListSerializer,
    UserRoleUpdateSerializer,
)

user_role_list_schema = extend_schema(
    tags=["User Roles"],
    summary="Listar asignaciones de roles",
    description=("Obtiene el listado de todas las asignaciones de roles a usuarios."),
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="UserRoleListResponse",
                data_serializer=UserRoleListSerializer,
                is_list=True,
            ),
            description="Listado de asignaciones de roles.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="No autenticado."
        ),
        403: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Permisos denegados."
        ),
    },
)

user_role_detail_schema = extend_schema(
    tags=["User Roles"],
    summary="Obtener asignación de rol",
    description="Obtiene la información detallada de una asignación de rol.",
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="UserRoleDetailResponse",
                data_serializer=UserRoleDetailSerializer,
            ),
            description="Información de la asignación.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="No autenticado."
        ),
        403: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Permisos denegados."
        ),
        404: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Asignación no encontrada."
        ),
    },
)

user_role_create_schema = extend_schema(
    tags=["User Roles"],
    summary="Asignar rol a usuario",
    description="Crea una nueva asignación de rol a un usuario.",
    request=UserRoleCreateSerializer,
    responses={
        201: OpenApiResponse(
            response=build_api_response_schema(
                name="UserRoleCreateResponse",
                data_serializer=UserRoleDetailSerializer,
            ),
            description="Asignación creada correctamente.",
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
)

user_role_update_schema = extend_schema(
    tags=["User Roles"],
    summary="Actualizar asignación",
    description="Actualiza completamente una asignación de rol.",
    request=UserRoleUpdateSerializer,
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="UserRoleUpdateResponse",
                data_serializer=UserRoleDetailSerializer,
            ),
            description="Asignación actualizada correctamente.",
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
            response=ApiErrorResponseSerializer, description="Asignación no encontrada."
        ),
    },
)

user_role_partial_update_schema = extend_schema(
    tags=["User Roles"],
    summary="Actualizar parcialmente una asignación",
    description="Actualiza uno o varios campos de una asignación.",
    request=UserRoleUpdateSerializer,
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="UserRolePartialUpdateResponse",
                data_serializer=UserRoleDetailSerializer,
            ),
            description="Asignación actualizada correctamente.",
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
            response=ApiErrorResponseSerializer, description="Asignación no encontrada."
        ),
    },
)

user_role_delete_schema = extend_schema(
    tags=["User Roles"],
    summary="Desactivar asignación",
    description="Realiza el borrado lógico de la asignación.",
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="UserRoleDeleteResponse",
            ),
            description="Asignación desactivada correctamente.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="No autenticado."
        ),
        403: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Permisos denegados."
        ),
        404: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Asignación no encontrada."
        ),
    },
)

user_role_restore_schema = extend_schema(
    tags=["User Roles"],
    summary="Restaurar asignación",
    description="Reactiva una asignación previamente desactivada.",
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="UserRoleRestoreResponse",
                data_serializer=UserRoleDetailSerializer,
            ),
            description="Asignación restaurada correctamente.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="No autenticado."
        ),
        403: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Permisos denegados."
        ),
        404: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Asignación no encontrada."
        ),
    },
)
