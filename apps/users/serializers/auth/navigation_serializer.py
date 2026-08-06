from rest_framework import serializers


class NavigationItemSerializer(serializers.Serializer):
    """
    Serializer recursivo para nodos del sidebar.
    """

    id = serializers.CharField()
    title = serializers.CharField()
    icon = serializers.CharField(required=False)
    route = serializers.CharField(required=False)
    permission = serializers.CharField(required=False)
    order = serializers.IntegerField()

    children = serializers.ListField(
        child=serializers.DictField(),
        required=False,
    )


class NavigationResponseSerializer(serializers.Serializer):
    """
    Serializer respuesta de navegación dinámica.
    """

    navigation = NavigationItemSerializer(many=True)
