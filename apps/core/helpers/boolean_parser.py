from typing import Optional

TRUE_VALUES = {
    "true",
    "1",
    "yes",
    "y",
    "on",
}

FALSE_VALUES = {
    "false",
    "0",
    "no",
    "n",
    "off",
}


def parse_bool(value: str | None) -> Optional[bool]:
    """
    Convierte un parámetro recibido desde la URL
    en un valor booleano.

    Ejemplos:

    ?is_active=true
    ?is_active=false
    ?is_active=1
    ?is_active=0

    Retorna:

        True
        False
        None
    """

    if value is None:
        return None

    value = value.strip().lower()

    if value in TRUE_VALUES:
        return True

    if value in FALSE_VALUES:
        return False

    return None
