from django.contrib.auth import authenticate
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.core.exceptions.custom_exceptions import (
    InvalidCredentialsException,
    InvalidTokenException,
    NoActiveRoleException,
    NoPermissionsException,
    UserInactiveException,
)
from apps.core.security.services import PermissionService
from apps.users.dto import LoginResult, MeResult
from apps.users.models import User


class AuthService:
    """
    Servicio encargado exclusivamente de la autenticación de usuarios.

    Responsabilidades:
        - Autenticar credenciales.
        - Validar estado del usuario, roles y permisos efectivos.
        - Generar y gestionar tokens JWT.
    """

    @staticmethod
    def login(username: str, password: str) -> LoginResult:
        """
        Autentica un usuario y genera los tokens JWT.

        Validaciones (en orden):
            1. Credenciales válidas.
            2. Usuario activo.
            3. Al menos un rol activo asignado.
            4. Al menos un permiso efectivo.

        Args:
            username:
                Nombre de usuario.
            password:
                Contraseña del usuario.

        Returns:
            ``LoginResult`` con usuario y tokens JWT.

        Raises:
            InvalidCredentialsException:
                Credenciales inválidas.
            UserInactiveException:
                Usuario inactivo.
            NoActiveRoleException:
                Sin roles activos.
            NoPermissionsException:
                Sin permisos efectivos.
        """

        user = authenticate(
            username=username,
            password=password,
        )

        if user is None:
            raise InvalidCredentialsException()

        if not user.is_active:
            raise UserInactiveException()

        if not PermissionService.has_any_active_role(user):
            raise NoActiveRoleException()

        effective_permissions = PermissionService.get_effective_permissions(user)

        if not PermissionService.has_any_permission(effective_permissions):
            raise NoPermissionsException()

        refresh = RefreshToken.for_user(user)

        return LoginResult(
            user=user,
            access_token=str(refresh.access_token),
            refresh_token=str(refresh),
        )

    @staticmethod
    def me(user: User) -> MeResult:
        """
        Retorna la información del usuario autenticado.

        Args:
            user:
                Usuario autenticado obtenido desde ``request.user``.

        Returns:
            ``MeResult`` con la información del usuario.
        """

        return MeResult(user=user)

    @staticmethod
    def refresh_token(validated_data: dict) -> dict:
        """Genera un nuevo Access Token a partir de un Refresh Token válido."""

        refresh_token = validated_data.get("refresh")
        from rest_framework.exceptions import ValidationError
        from rest_framework_simplejwt.serializers import TokenRefreshSerializer

        try:
            serializer = TokenRefreshSerializer(data={"refresh": refresh_token})
            serializer.is_valid(raise_exception=True)
            return serializer.validated_data
        except (TokenError, ValidationError):
            raise InvalidTokenException()

    @staticmethod
    def logout(refresh_token: str, user: User) -> None:
        """Invalida un Refresh Token incluyéndolo en la Blacklist."""

        try:
            token = RefreshToken(refresh_token)

            from rest_framework_simplejwt.settings import api_settings

            user_id_claim = api_settings.USER_ID_CLAIM

            if str(token.payload.get(user_id_claim)) != str(user.id_user):
                raise InvalidTokenException()

            token.blacklist()
        except TokenError:
            # Según RFC 7009, revocar un token ya revocado o inválido debe retornar 200 OK.
            pass
