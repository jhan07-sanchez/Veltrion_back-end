"""
Servicio de métricas para el Dashboard.
"""

from typing import Any
from django.utils import timezone

from apps.users.models import User, Role
from apps.customers.models import Customer
from apps.suppliers.models import Supplier


class DashboardMetricsService:
    """
    Servicio encargado de calcular las métricas para los widgets del dashboard.
    """

    @staticmethod
    def get_metrics(visible_widgets: list[str]) -> list[dict[str, Any]]:
        """
        Calcula y devuelve los valores para los widgets proporcionados.
        """
        metrics = []
        now = timezone.now()

        for code in visible_widgets:
            value: Any = 0

            if code == "users_total":
                value = User.objects.count()
            elif code == "users_active":
                value = User.objects.filter(is_active=True).count()
            elif code == "roles_distribution":
                value = Role.objects.count()
            elif code == "customers_total":
                value = Customer.objects.count()
            elif code == "customers_recent":
                value = Customer.objects.filter(
                    created_at__year=now.year, created_at__month=now.month
                ).count()
            elif code == "suppliers_active":
                value = Supplier.objects.filter(is_active=True).count()
            elif code == "erp_activity":
                value = [
                    {"label": "Usuarios activos", "value": User.objects.filter(is_active=True).count(), "icon": "fas fa-user-check", "color": "success"},
                    {"label": "Clientes", "value": Customer.objects.count(), "icon": "fas fa-user-tie", "color": "info"},
                    {"label": "Proveedores", "value": Supplier.objects.filter(is_active=True).count(), "icon": "fas fa-truck", "color": "secondary"},
                ]
            else:
                # Widgets para módulos no desarrollados aún (ventas, compras, etc.)
                list_widgets = [
                    "roles_distribution", "sales_monthly", "purchases_monthly", 
                    "needs_attention", "top_selling_products", "latest_sales"
                ]
                if code in list_widgets:
                    value = []
                else:
                    value = 0

            metrics.append({"code": code, "value": value})

        return metrics
