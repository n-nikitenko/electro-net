from django.contrib import admin

from .models import NetworkNode


@admin.action(description="Обнулить задолженность перед поставщиком")
def clear_debt(modeladmin, request, queryset):
    """обнуление задолженности перед поставщиком"""
    queryset.update(debt_to_supplier=0)

    # Вывод сообщения в интерфейсе админ-панели
    modeladmin.message_user(request, "Задолженность перед поставщиком успешно обнулена для выбранных объектов.")


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier', 'debt_to_supplier', 'created_at')
    list_filter = ('city',)
    actions = [clear_debt]
