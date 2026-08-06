from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from apps.core.docs.api_response_schema import build_api_response_schema
from apps.core.docs.error_schemas import (
    ApiErrorResponseSerializer,
    ValidationErrorResponseSerializer,
)
from apps.users.serializers.auth.login_serializer import (
    LoginResponseSerializer,
    AuthLoginSerializer,
)
from apps.users.serializers.auth.me_serializer import MeResponseSerializer
from apps.users.serializers.auth.auth_refresh_response_serializer import (
    AuthRefreshResponseSerializer,
)


login_schema = extend_schema(
    tags=["Authentication"],
    summary="Iniciar sesión",
    description=(
        "Autentica un usuario utilizando su nombre de usuario y contraseña. "
        "Si las credenciales son válidas, retorna la información del usuario "
        "junto con un Access Token y un Refresh Token JWT."
    ),
    request=AuthLoginSerializer,
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="AuthLoginResponse",
                data_serializer=LoginResponseSerializer,
            ),
            description="Inicio de sesión exitoso.",
        ),
        400: OpenApiResponse(
            response=ValidationErrorResponseSerializer,
            description="Credenciales inválidas (error de validación).",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="Usuario o contraseña incorrectos.",
        ),
    },
    examples=[
        OpenApiExample(
            name="Ejemplo de Login Exitoso",
            request_only=True,
            value={
                "username": "software_veltrion",
                "password": "12345678",
            },
        ),
    ],
)

me_schema = extend_schema(
    tags=["Authentication"],
    summary="Obtener usuario autenticado",
    description=(
        "Retorna la información del usuario autenticado "
        "a partir del Access Token enviado en el encabezado Authorization."
    ),
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="AuthMeResponse",
                data_serializer=MeResponseSerializer,
            ),
            description="Información del usuario autenticado.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="Token inválido o expirado.",
        ),
    },
)

refresh_schema = extend_schema(
    tags=["Authentication"],
    summary="Renovar Access Token",
    description="Genera un nuevo Access Token a partir de un Refresh Token válido.",
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(
                name="AuthRefreshResponse",
                data_serializer=AuthRefreshResponseSerializer,
            ),
            description="Token renovado exitosamente.",
        ),
        400: OpenApiResponse(
            response=ValidationErrorResponseSerializer,
            description="Token no enviado o inválido.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="Token expirado o no válido para renovación.",
        ),
    },
)

logout_schema = extend_schema(
    tags=["Authentication"],
    summary="Cerrar sesión",
    description="Invalida el Refresh Token proporcionado.",
    responses={
        200: OpenApiResponse(
            response=build_api_response_schema(name="AuthLogoutResponse"),
            description="Sesión cerrada correctamente.",
        ),
        400: OpenApiResponse(
            response=ValidationErrorResponseSerializer,
            description="Token no proporcionado.",
        ),
        401: OpenApiResponse(
            response=ApiErrorResponseSerializer,
            description="No autenticado.",
        ),
    },
)
