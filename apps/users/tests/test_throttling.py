from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class ThrottlingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("auth-login")
        self.refresh_url = reverse("auth-refresh")
        # Clear cache to reset throttle counters
        cache.clear()

    def test_login_throttling(self):
        """Test that login limits to 5 attempts per minute"""
        # Make 5 failed attempts
        for _ in range(5):
            res = self.client.post(
                self.login_url, {"username": "testuser", "password": "wrongpassword"}
            )
            self.assertNotEqual(res.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

        # The 6th attempt should be throttled
        res = self.client.post(
            self.login_url, {"username": "testuser", "password": "wrongpassword"}
        )
        self.assertEqual(res.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_refresh_throttling(self):
        """Test that refresh limits to 10 attempts per minute"""
        # Make 10 attempts
        for _ in range(10):
            res = self.client.post(self.refresh_url, {"refresh": "invalid_token"})
            self.assertNotEqual(res.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

        # The 11th attempt should be throttled
        res = self.client.post(self.refresh_url, {"refresh": "invalid_token"})
        self.assertEqual(res.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
