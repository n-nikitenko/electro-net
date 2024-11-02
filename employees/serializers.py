from rest_framework import serializers

from employees.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
        )
        optional_fields = ("email", "first_name", "last_name")
        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
        }


class EmployeeUpdateSerializer(EmployeeSerializer):
    username = serializers.CharField(required=False, min_length=1)
    password = serializers.CharField(
        write_only=True, required=False, style={"input_type": "password"}, min_length=1
    )

    class Meta:
        model = Employee
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
        )
        optional_fields = ("email", "first_name", "last_name", "password", "username")
        extra_kwargs = {
            "id": {"read_only": True},
        }
