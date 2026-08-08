from django.test import TestCase
from rest_framework import status

from apps.core.exceptions.exception_handler import custom_exception_handler


class ExceptionHandlerTests(TestCase):
    def test_internal_server_error_hides_details(self):
        # Simulate a 500 error
        exc = Exception("Secret Database Error that should not be visible")

        # Call the exception handler directly since testing the whole middleware is harder
        response = custom_exception_handler(exc, None)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Check that the error details are hidden
        self.assertNotIn("Secret Database Error", str(response.data))
        self.assertEqual(
            response.data["message"], "Ha ocurrido un error interno en el servidor."
        )
        self.assertIsNone(response.data["errors"])
