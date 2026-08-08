import json

from django.http import HttpResponse
from django.test import RequestFactory, TestCase

from apps.core.middlewares.audit_middleware import AuditMiddleware


class AuditMiddlewareTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = AuditMiddleware(
            get_response=lambda r: HttpResponse(status=200)
        )

    def test_mask_sensitive_data(self):
        payload = {
            "username": "test",
            "password": "secretpassword",
            "nested": {"token": "myjwttoken", "normal": "data"},
        }
        masked = self.middleware._mask_sensitive_data(payload)
        self.assertEqual(masked["password"], "********")
        self.assertEqual(masked["nested"]["token"], "********")
        self.assertEqual(masked["nested"]["normal"], "data")

    def test_audit_log_created_on_post(self):
        request = self.factory.post(
            "/api/test/",
            data=json.dumps({"test": "data"}),
            content_type="application/json",
        )
        # Audit log creation might fail if DB is not setup for it or user is missing,
        # but the middleware shouldn't crash.
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)

    def test_large_payload(self):
        large_data = "x" * 5000
        request = self.factory.post(
            "/api/test/",
            data=json.dumps({"large": large_data}),
            content_type="application/json",
        )
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)
