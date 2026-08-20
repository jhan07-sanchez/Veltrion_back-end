from rest_framework import serializers


class DashboardWidgetSerializer(serializers.Serializer):
    code = serializers.CharField(read_only=True)
    value = serializers.IntegerField(read_only=True)


class DashboardResponseSerializer(serializers.Serializer):
    """
    Serializer de respuesta del endpoint ``GET /security/dashboard``.

    Serializa únicamente la configuración de widgets del dashboard y sus valores.
    """

    widgets = serializers.ListField(
        child=DashboardWidgetSerializer(),
        read_only=True,
    )

    def to_representation(self, instance: dict) -> dict:
        """Convierte el resultado del ``DashboardBuilder`` en JSON."""

        return {"widgets": instance.get("widgets", [])}
