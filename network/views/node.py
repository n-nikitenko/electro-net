from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions

from network.filters import NetworkNodeCountryFilter
from network.models import NetworkNode
from network.paginators import NetworkPaginator
from network.permissions import IsActiveEmployeePermission
from network.serializers import NetworkNodeSerializer
from network.serializers.node import NetworkNodeUpdateSerializer

node_update_responses = {
    "400": openapi.Response(
        description="Ошибка валидации",
        examples={
            "application/json": {
                "supplier": ["Нельзя в качестве поставщика указать этот же узел сети",
                             "Узел сети не может находиться на уровне выше 2."],
            }
        }
    )
}


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Получение списка узлов сети", tags=["Узлы сети"]
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Регистрация узла сети", tags=["Узлы сети"]
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Получение данных узла сети по id", tags=["Узлы сети"]
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Обновление данных узла сети по id", tags=["Узлы сети"],
        responses=node_update_responses
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Обновление данных узла сети по id", tags=["Узлы сети"],
        responses=node_update_responses
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Удаление данных узла сети по id", tags=["Узлы сети"]
    ),
)
class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all().select_related('supplier').prefetch_related('products')
    pagination_class = NetworkPaginator
    permission_classes = [permissions.IsAuthenticated, IsActiveEmployeePermission]
    filterset_class = NetworkNodeCountryFilter

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return NetworkNodeUpdateSerializer
        else:
            return NetworkNodeSerializer
