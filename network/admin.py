from django.contrib import admin

from .forms import NetworkNodeAdminForm
from .models import NetworkNode, Product


@admin.action(description="Обнулить задолженность перед поставщиком")
def clear_debt(modeladmin, request, queryset):
    """обнуление задолженности перед поставщиком"""
    queryset.update(debt_to_supplier=0)

    # Вывод сообщения в интерфейсе админ-панели
    modeladmin.message_user(
        request,
        "Задолженность перед поставщиком успешно обнулена для выбранных объектов.",
    )


class ProductInline(admin.TabularInline):
    model = Product


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    form = NetworkNodeAdminForm
    inlines = [
        ProductInline,
    ]
    list_display = (
        "id",
        "name",
        "supplier",
        "debt_to_supplier",
        "created_at",
        "node_type",
    )
    list_filter = ("city",)

    actions = [clear_debt]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "model", "release_date", "network_node")
    list_filter = ("network_node",)
