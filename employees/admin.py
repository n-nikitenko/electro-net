from django.contrib import admin

from employees.models import Employee


@admin.register(Employee)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_staff",
        "last_login",
        "date_joined",
    )
