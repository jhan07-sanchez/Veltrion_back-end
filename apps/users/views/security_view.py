from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.core.security.services import SecurityService
from apps.core.utils.api_response import ApiResponse
from apps.users.docs.security_docs import (
    dashboard_schema,
    navigation_schema,
    security_context_schema,
)
from apps.users.serializers.auth.dashboard_serializer import DashboardResponseSerializer
from apps.users.serializers.auth.navigation_serializer import NavigationResponseSerializer
from apps.users.serializers.auth.security_context_serializer import (
    SecurityContextResponseSerializer,
)


@extend_schema(
    tags=["Security"],
    summary="Contexto de autorización",
    description=(
        "Retorna roles, permisos efectivos y acciones del usuario autenticado."
    ),
    responses={status.HTTP_200_OK: SecurityContextResponseSerializer},
)
class SecurityContextView(APIView):
    """Endpoint del contexto completo de autorización."""

    permission_classes = [IsAuthenticated]

    @security_context_schema
    def get(self, request):
        """Retorna roles, permisos y acciones efectivas."""

        context_result = SecurityService.get_authorization_context(request.user)
        serializer = SecurityContextResponseSerializer(context_result)

        return ApiResponse.success(
            message="Contexto de seguridad obtenido correctamente.",
            code="SECURITY_CONTEXT_FETCHED",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["Security"],
    summary="Navegación dinámica",
    description="Retorna el árbol de navegación filtrado por permisos.",
    responses={status.HTTP_200_OK: NavigationResponseSerializer},
)
class SecurityNavigationView(APIView):
    """Endpoint del árbol de navegación del usuario autenticado."""

    permission_classes = [IsAuthenticated]

    @navigation_schema
    def get(self, request):
        """Retorna únicamente el árbol de navegación."""

        navigation = SecurityService.get_navigation(request.user)

        print("FINAL NAVIGATION:")
        print(navigation)
        print(type(navigation))
        serializer = NavigationResponseSerializer(
            {
                "navigation": navigation
            }
        )

        return ApiResponse.success(
            message="Navegación obtenida correctamente.",
            code="SECURITY_NAVIGATION_FETCHED",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["Security"],
    summary="Dashboard dinámico",
    description="Retorna los widgets del dashboard según permisos del usuario.",
    responses={status.HTTP_200_OK: DashboardResponseSerializer},
)
class SecurityDashboardView(APIView):
    """Endpoint de configuración del dashboard del usuario autenticado."""

    permission_classes = [IsAuthenticated]

    @dashboard_schema
    def get(self, request):
        """Retorna únicamente la configuración de widgets del dashboard."""

        dashboard = SecurityService.get_dashboard(request.user)
        serializer = DashboardResponseSerializer(dashboard)

        return ApiResponse.success(
            message="Dashboard obtenido correctamente.",
            code="SECURITY_DASHBOARD_FETCHED",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )
