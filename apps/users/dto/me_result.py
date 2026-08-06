from dataclasses import dataclass

from apps.users.models import User


@dataclass(frozen=True, slots=True)
class MeResult:
    """
    DTO del caso de uso ``GET /auth/me``.

    Representa únicamente la información del usuario autenticado.
    """

    user: User
