from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions

from network.filters import NetworkProductCountryFilter
from network.models import Product
from network.paginators import NetworkPaginator
from network.permissions import IsActiveEmployeePermission
from network.serializers import ProductSerializer


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Получение списка продуктов", tags=["Продукты"]
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Регистрация продукта", tags=["Продукты"]
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Получение данных продукта по id", tags=["Продукты"]
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Обновление данных продукта по id", tags=["Продукты"]
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Обновление данных продукта по id", tags=["Продукты"]
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Удаление данных продукта по id", tags=["Продукты"]
    ),
)
class NetworkProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('network_node')
    pagination_class = NetworkPaginator
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveEmployeePermission]
    filterset_class = NetworkProductCountryFilter
