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
from apps.users.serializers.user_serializer import (
    UserCreateSerializer,
    UserDetailSerializer,
    UserListSerializer,
    UserUpdateSerializer,
)

user_list_schema = extend_schema(
    tags=["Users"],
    summary="Listar usuarios",
    description=("Obtiene el listado de todos los usuarios registrados en el sistema."),
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="UserListResponse",
                data_serializer=UserListSerializer,
                is_list=True,
            ),
            description="Listado de usuarios.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="No autenticado."
        ),
        403: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Permisos denegados."
        ),
    },
)

user_detail_schema = extend_schema(
    tags=["Users"],
    summary="Obtener usuario",
    description=("Obtiene toda la informacion de un usuario especifico."),
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="UserDetailResponse",
                data_serializer=UserDetailSerializer,
            ),
            description="Informacion del usuario.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="No autenticado."
        ),
        403: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Permisos denegados."
        ),
        404: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Usuario no encontrado."
        ),
    },
)

user_create_schema = extend_schema(
    tags=["Users"],
    summary="Crear usuario",
    description="Crea un nuevo usuario dentro del sistema.",
    request=UserCreateSerializer,
    responses={
        201: OpenApiResponse(
            response=build_api_response_schema(
                name="UserCreateResponse",
                data_serializer=UserDetailSerializer,
            ),
            description="Usuario creado correctamente.",
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
            "Crear Usuario",
            request_only=True,
            value={
                "username": "juanperez",
                "password": "Admin123*",
                "first_name": "Juan",
                "last_name": "Pérez",
                "email": "juan@gmail.com",
                "document_number": "123456789",
                "phone_number": "3001234567",
            },
        )
    ],
)

user_update_schema = extend_schema(
    tags=["Users"],
    summary="Actualizar usuario",
    description="Actualiza completamente un usuario.",
    request=UserUpdateSerializer,
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="UserUpdateResponse",
                data_serializer=UserDetailSerializer,
            ),
            description="Usuario actualizado correctamente.",
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
            response=ApiErrorResponseSerializer, description="Usuario no encontrado."
        ),
    },
)

user_partial_update_schema = extend_schema(
    tags=["Users"],
    summary="Actualizar parcialmente un usuario",
    description="Actualiza uno o varios campos del usuario.",
    request=UserUpdateSerializer,
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="UserPartialUpdateResponse",
                data_serializer=UserDetailSerializer,
            ),
            description="Usuario actualizado correctamente.",
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
            response=ApiErrorResponseSerializer, description="Usuario no encontrado."
        ),
    },
)

user_delete_schema = extend_schema(
    tags=["Users"],
    summary="Desactivar usuario",
    description=(
        "Realiza el borrado lógico del usuario. No elimina físicamente el registro."
    ),
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="UserDeleteResponse",
            ),
            description="Usuario desactivado correctamente.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="No autenticado."
        ),
        403: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Permisos denegados."
        ),
        404: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Usuario no encontrado."
        ),
    },
)

user_restore_schema = extend_schema(
    tags=["Users"],
    summary="Restaurar usuario",
    description="Reactiva un usuario previamente desactivado.",
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="UserRestoreResponse",
                data_serializer=UserDetailSerializer,
            ),
            description="Usuario restaurado correctamente.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="No autenticado."
        ),
        403: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Permisos denegados."
        ),
        404: OpenApiResponse(
            response=ApiErrorResponseSerializer, description="Usuario no encontrado."
        ),
    },
)
