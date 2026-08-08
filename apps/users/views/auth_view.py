from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from apps.core.utils.api_response import ApiResponse
from apps.users.docs.auth_docs import (
    login_schema,
    logout_schema,
    me_schema,
    refresh_schema,
)
from apps.users.serializers.auth.auth_logout_serializer import AuthLogoutSerializer
from apps.users.serializers.auth.auth_refresh_serializer import AuthRefreshSerializer
from apps.users.serializers.auth.login_serializer import (
    AuthLoginSerializer,
    LoginResponseSerializer,
)
from apps.users.serializers.auth.me_serializer import MeResponseSerializer
from apps.users.services.auth_service import AuthService


class AuthLoginView(APIView):
    """Endpoint encargado del inicio de sesión."""

    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth_login"

    @login_schema
    def post(self, request):
        """Autentica un usuario y devuelve usuario con tokens JWT."""

        serializer = AuthLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        login_result = AuthService.login(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        response_serializer = LoginResponseSerializer(login_result)

        return ApiResponse.success(
            message="Inicio de sesión exitoso.",
            code="LOGIN_SUCCESS",
            data=response_serializer.data,
            status_code=status.HTTP_200_OK,
        )


class MeView(APIView):
    """Endpoint que retorna la información del usuario autenticado."""

    permission_classes = [IsAuthenticated]

    @me_schema
    def get(self, request):
        """Retorna únicamente la información del usuario autenticado."""

        me_result = AuthService.me(request.user)
        serializer = MeResponseSerializer(me_result)

        return ApiResponse.success(
            message="Información del usuario obtenida correctamente.",
            code="USER_ME_FETCHED",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


class AuthRefreshView(APIView):
    """Endpoint para renovar el Access Token."""

    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth_refresh"

    @refresh_schema
    def post(self, request):
        serializer = AuthRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = AuthService.refresh_token(serializer.validated_data)

        return ApiResponse.success(
            message="Token renovado correctamente.",
            code="TOKEN_REFRESHED",
            data=data,
            status_code=status.HTTP_200_OK,
        )


class AuthLogoutView(APIView):
    """Endpoint encargado del cierre de sesión."""

    permission_classes = [IsAuthenticated]

    @logout_schema
    def post(self, request):
        """Invalida el Refresh Token para cerrar la sesión."""

        serializer = AuthLogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        AuthService.logout(
            refresh_token=serializer.validated_data["refresh"],
            user=request.user,
        )

        return ApiResponse.success(
            message="Cierre de sesión exitoso.",
            code="LOGOUT_SUCCESS",
            status_code=status.HTTP_200_OK,
        )
