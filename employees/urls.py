from django.urls import include, path
from rest_framework.routers import SimpleRouter

from employees.apps import EmployeesConfig
from employees.views import (EmployeeTokenObtainPairView,
                             EmployeeTokenRefreshView, EmployeeViewSet)

app_name = EmployeesConfig.name

router = SimpleRouter()
router.register(r"employees", EmployeeViewSet, basename="employee")

urlpatterns = [
    path(
        "login/",
        EmployeeTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("token/refresh/", EmployeeTokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
