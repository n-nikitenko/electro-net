from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

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
        "supplier_link",
        "debt_to_supplier",
        "created_at",
        "node_type",
    )

    def supplier_link(self, obj):
        if obj.supplier:
            return mark_safe(
                u'<a href="{0}">{1}</a>'.format(reverse('admin:network_networknode_change', args=(obj.supplier.pk,)),
                                                obj.supplier))
        else:
            return "-"

    supplier_link.allow_tags = True
    supplier_link.admin_order_field = 'supplier'
    supplier_link.short_description = NetworkNode._meta.get_field('supplier').verbose_name.title()

    list_filter = ("city",)

    actions = [clear_debt]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "model", "release_date", "supplier_link", "supplier_city")
    list_filter = ("network_node",)

    def supplier_link(self, obj):
        if obj.network_node:
            return mark_safe(
                u'<a href="{0}">{1}</a>'.format(
                    reverse('admin:network_networknode_change', args=(obj.network_node.pk,)),
                    obj.network_node))
        else:
            return "-"

    supplier_link.allow_tags = True
    supplier_link.admin_order_field = 'network_node'
    supplier_link.short_description = Product._meta.get_field('network_node').verbose_name.title()

    def supplier_city(self, obj):
        if obj.network_node:
            return obj.network_node.city
        else:
            return "-"

    supplier_city.admin_order_field = 'network_node__city'
    supplier_city.short_description = "Город  поставщика"
