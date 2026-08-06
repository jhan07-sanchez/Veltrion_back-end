from rest_framework.pagination import PageNumberPagination

from apps.core.utils.api_response import ApiResponse


class CustomPagination(PageNumberPagination):
    """
    Paginación personalizada para toda la API.

    Todas las respuestas paginadas mantienen el mismo
    formato utilizado por ApiResponse.
    """

    page_size = 10

    page_size_query_param = "page_size"

    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Retorna una respuesta paginada con el formato
        estándar de la API.
        """

        return ApiResponse.success(
            message="Datos obtenidos correctamente.",
            data={
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "page": self.page.number,
                "total_pages": self.page.paginator.num_pages,
                "page_size": self.get_page_size(self.request),
                "results": data,
            },
        )
