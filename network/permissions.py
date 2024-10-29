from rest_framework import permissions


class IsActiveEmployeePermission(permissions.BasePermission):
    """проверка, является ли сотрудник активным"""

    def has_object_permission(self, request, view, obj):
        return request.user.is_active
