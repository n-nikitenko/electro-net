from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from employees.forms import EmployeeCreationForm
from employees.models import Employee


@admin.register(Employee)
class UserAdmin(UserAdmin):
    add_form = EmployeeCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'first_name', 'last_name', 'is_active', 'is_staff'),
        }),
    )
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
