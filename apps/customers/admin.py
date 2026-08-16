from django.contrib import admin

from apps.customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "id_customer",
        "document_type",
        "document_number",
        "first_name",
        "last_name",
        "business_name",
        "email",
        "is_active",
    )

    search_fields = (
        "document_number",
        "first_name",
        "last_name",
        "business_name",
        "email",
    )

    list_filter = (
        "is_active",
        "document_type",
    )

    ordering = ("id_customer",)

    fieldsets = (
        (
            "Información principal",
            {
                "fields": (
                    "document_type",
                    "document_number",
                    "first_name",
                    "last_name",
                    "business_name",
                )
            },
        ),
        (
            "Información de contacto",
            {
                "fields": (
                    "email",
                    "phone",
                    "mobile",
                    "address",
                    "city",
                    "country",
                )
            },
        ),
        (
            "Estado y Notas",
            {
                "fields": (
                    "is_active",
                    "notes",
                )
            },
        ),
        (
            "Fechas importantes",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    exclude = ("deleted_at",)

    def get_queryset(self, request):
        """Muestra todos los clientes, incluyendo los eliminados lógicamente."""
        return Customer.all_objects.all()
