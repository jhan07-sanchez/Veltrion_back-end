from django.urls import include, path


urlpatterns = [
    path("", include("apps.users.urls")),
    path("", include("apps.customers.urls")),
    path("", include("apps.suppliers.urls")),
]
