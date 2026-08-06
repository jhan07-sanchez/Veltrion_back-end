from django.core.validators import RegexValidator

document_number_validator = RegexValidator(
    regex=r"^[0-9]+$", message="El número de documento solo puede contener números."
)
