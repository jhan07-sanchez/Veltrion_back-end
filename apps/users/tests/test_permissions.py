from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.core.security.services import PermissionService
from apps.users.models import Role, User, UserRole


class PermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
            email="test@example.com",
            document_number="123456789",
        )
        self.role = Role.objects.create(
            role_name="admin_role", permissions={"users.view": True}
        )
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)
        # Assuming the Users API requires "users.view"
        self.users_url = reverse("users-list")

    def test_permission_service_has_any_active_role(self):
        self.assertTrue(PermissionService.has_any_active_role(self.user))
        self.role.is_active = False
        self.role.save()
        self.assertFalse(PermissionService.has_any_active_role(self.user))

    def test_permission_service_get_effective_permissions(self):
        perms = PermissionService.get_effective_permissions(self.user)
        self.assertTrue(perms.get("users.view"))

        # Test disabled role
        self.role.is_active = False
        self.role.save()
        perms = PermissionService.get_effective_permissions(self.user)
        self.assertFalse(perms.get("users.view", False))

    def test_api_access_with_permission(self):
        # We must authenticate first
        login_res = self.client.post(
            reverse("auth-login"),
            {"username": "testuser", "password": "testpassword123"},
        )
        access_token = login_res.data["data"]["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

        # Access allowed
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Now revoke permission
        self.role.permissions = {"users.view": False}
        self.role.save()

        # Access denied
        response2 = self.client.get(self.users_url)
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
