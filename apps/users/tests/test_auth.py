from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.models import Role, User, UserRole


class AuthTests(TestCase):
    def setUp(self):
        from django.core.cache import cache

        cache.clear()

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
        self.login_url = reverse("auth-login")
        self.refresh_url = reverse("auth-refresh")
        self.logout_url = reverse("auth-logout")

    def test_login_success(self):
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "testpassword123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data["data"])
        self.assertIn("refresh_token", response.data["data"])

    def test_login_invalid_credentials(self):
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["code"], "AUTHENTICATION_FAILED")

    def test_login_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "testpassword123"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_no_role(self):
        self.user_role.delete()  # soft delete
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "testpassword123"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_no_permissions(self):
        self.role.permissions = {}
        self.role.save()
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "testpassword123"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_jwt_refresh_and_logout(self):
        login_res = self.client.post(
            self.login_url, {"username": "testuser", "password": "testpassword123"}
        )
        refresh_token = login_res.data["data"]["refresh_token"]
        access_token = login_res.data["data"]["access_token"]

        refresh_res = self.client.post(self.refresh_url, {"refresh": refresh_token})
        self.assertEqual(refresh_res.status_code, status.HTTP_200_OK)
        new_refresh = refresh_res.data["data"].get("refresh_token", refresh_token)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
        logout_res = self.client.post(self.logout_url, {"refresh": new_refresh})
        self.assertEqual(logout_res.status_code, status.HTTP_200_OK)

        fail_res = self.client.post(self.refresh_url, {"refresh": new_refresh})
        self.assertEqual(fail_res.status_code, status.HTTP_401_UNAUTHORIZED)

        # Verify old token from rotation is also invalid
        if new_refresh != refresh_token:
            old_fail_res = self.client.post(
                self.refresh_url, {"refresh": refresh_token}
            )
            self.assertEqual(old_fail_res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_logout_other_user(self):
        login_res = self.client.post(
            self.login_url, {"username": "testuser", "password": "testpassword123"}
        )
        refresh_token = login_res.data["data"]["refresh_token"]

        user2 = User.objects.create_user(
            username="hacker",
            password="testpassword123",
            email="hack@hack.com",
            document_number="987654321",
        )
        UserRole.objects.create(user=user2, role=self.role)
        login_res_2 = self.client.post(
            self.login_url, {"username": "hacker", "password": "testpassword123"}
        )
        access_token_2 = login_res_2.data["data"]["access_token"]

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token_2)
        # Try to logout with first user's refresh token
        logout_res = self.client.post(self.logout_url, {"refresh": refresh_token})
        # Should raise 401 Unauthorized or 400 because token does not belong to user
        self.assertEqual(logout_res.status_code, status.HTTP_401_UNAUTHORIZED)
