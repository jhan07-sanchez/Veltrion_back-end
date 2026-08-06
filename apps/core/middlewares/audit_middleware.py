import json
import logging

from django.utils.deprecation import MiddlewareMixin
from apps.core.models.audit_log import AuditLog

logger = logging.getLogger(__name__)


class AuditMiddleware(MiddlewareMixin):
    """
    Middleware que intercepta peticiones HTTP para registrar un Audit Trail.
    """

    SENSITIVE_KEYS = ["password", "token", "access", "refresh", "secret"]

    def __call__(self, request):
        payload = {}
        content_type = request.META.get("CONTENT_TYPE", "")

        # Si es multipart/form-data, evitamos leer request.body para no corromper 
        # el stream ni romper la carga de archivos en las vistas.
        if "multipart/form-data" in content_type:
            payload = {"detail": "Multipart form data omited."}
        else:
            try:
                body_bytes = request.body
                if body_bytes:
                    body_str = body_bytes.decode("utf-8")
                    payload = json.loads(body_str)
            except (json.JSONDecodeError, UnicodeDecodeError, AttributeError, Exception):
                payload = {}

        masked_payload = self._mask_sensitive_data(payload)

        # Continúa la ejecución normal de la petición (aquí se llama a la vista)
        response = self.get_response(request)

        # Solo guardaremos registro de acciones que mutan datos (se excluye GET, OPTIONS, etc.)
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            
            # En DRF, request.user se establece a veces tarde o queda en un wrapper. 
            # Si el usuario se autenticó, intentaremos obtenerlo.
            user = getattr(request, "user", None)
            if user and not user.is_authenticated:
                user = None
                
            ip_address = self._get_client_ip(request)

            try:
                AuditLog.objects.create(
                    user=user,
                    method=request.method,
                    path=request.path,
                    ip_address=ip_address,
                    user_agent=request.META.get("HTTP_USER_AGENT", ""),
                    status_code=response.status_code,
                    payload=masked_payload,
                )
            except Exception as e:  # noqa: BLE001
                logger.error(f"No se pudo guardar el registro de auditoría: {e!s}")

        return response

    def _mask_sensitive_data(self, data):
        """
        Enmascara campos sensibles recursivamente dentro del payload.
        """
        if isinstance(data, dict):
            masked = {}
            for k, v in data.items():
                # Comprobamos si la clave contiene palabras sensibles
                if any(sensible in k.lower() for sensible in self.SENSITIVE_KEYS):
                    masked[k] = "********"
                else:
                    masked[k] = self._mask_sensitive_data(v)
            return masked
        elif isinstance(data, list):
            return [self._mask_sensitive_data(item) for item in data]
        else:
            return data

    def _get_client_ip(self, request):
        """
        Obtiene la IP real del cliente considerando posibles proxies.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
