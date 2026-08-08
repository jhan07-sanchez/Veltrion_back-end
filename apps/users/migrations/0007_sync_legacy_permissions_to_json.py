# Generated manually — sincroniza booleanos legacy al JSON de permisos.

from django.db import migrations


def sync_legacy_booleans_to_permissions_json(apps, schema_editor):
    Role = apps.get_model("users", "Role")

    legacy_map = {
        "users_create": "users.create",
        "users_read": "users.view",
        "users_update": "users.update",
        "users_delete": "users.delete",
        "user_roles_create": "user_roles.create",
        "user_roles_read": "user_roles.view",
        "user_roles_update": "user_roles.update",
        "user_roles_delete": "user_roles.delete",
        "customers_create": "customers.create",
        "customers_read": "customers.view",
        "customers_update": "customers.update",
        "customers_delete": "customers.delete",
        "suppliers_create": "suppliers.create",
        "suppliers_read": "suppliers.view",
        "suppliers_update": "suppliers.update",
        "suppliers_delete": "suppliers.delete",
        "categories_create": "categories.create",
        "categories_read": "categories.view",
        "categories_update": "categories.update",
        "categories_delete": "categories.delete",
        "products_create": "products.create",
        "products_read": "products.view",
        "products_update": "products.update",
        "products_delete": "products.delete",
        "inventory_create": "inventory.create",
        "inventory_read": "inventory.view",
        "inventory_update": "inventory.update",
        "inventory_delete": "inventory.delete",
        "purchases_create": "purchases.create",
        "purchases_read": "purchases.view",
        "purchases_update": "purchases.update",
        "purchases_delete": "purchases.delete",
        "sales_create": "sales.create",
        "sales_read": "sales.view",
        "sales_update": "sales.update",
        "sales_delete": "sales.delete",
        "reports_read": "reports.view",
        "settings_update": "settings.update",
    }

    for role in Role.objects.all():
        permissions = dict(role.permissions or {})
        updated = False

        for field_name, code in legacy_map.items():
            if getattr(role, field_name, False) and not permissions.get(code):
                permissions[code] = True
                updated = True

        if updated:
            role.permissions = permissions
            role.save(update_fields=["permissions"])


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0006_add_permissions_json_field"),
    ]

    operations = [
        migrations.RunPython(
            sync_legacy_booleans_to_permissions_json,
            migrations.RunPython.noop,
        ),
    ]
