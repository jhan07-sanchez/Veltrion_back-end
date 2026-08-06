from dataclasses import dataclass

from apps.users.models import User


@dataclass(frozen=True, slots=True)
class LoginResult:
    """
    DTO del caso de uso de autenticación.

    Representa únicamente el resultado del login:
    usuario autenticado y tokens JWT generados.
    """

    user: User
    access_token: str
    refresh_token: str
