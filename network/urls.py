from django.urls import include, path
from rest_framework.routers import SimpleRouter

from network.apps import NetworkConfig
from network.views import NetworkNodeViewSet
from network.views import NetworkProductViewSet

app_name = NetworkConfig.name

router = SimpleRouter()
router.register(r"nodes", NetworkNodeViewSet, basename="nodes")
router.register(r"products", NetworkProductViewSet, basename="products")

urlpatterns = [
    path("", include(router.urls)),
]
