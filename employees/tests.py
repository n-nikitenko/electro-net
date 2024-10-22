from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from employees.models import Employee

User = get_user_model()


class EmployeeAPITestCase(APITestCase):

    def setUp(self):
        """Создание тестового сотрудника для получения токенов"""

        self.employee = Employee.objects.create_user(
            username="testuser", password="testpass"
        )

        self.employee_list_url = reverse("employees:employee-list")
        self.employee_detail_url = reverse(
            "employees:employee-detail", args=(self.employee.pk,)
        )

    def test_get_employees_list(self):
        """Тест получения списка сотрудников"""
        self.client.force_authenticate(user=self.employee)

        # Создание дополнительных сотрудников
        Employee.objects.create_user(username="employee1", password="password1")
        Employee.objects.create_user(username="employee2", password="password2")

        response = self.client.get(self.employee_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)

    def test_create_employee(self):
        """Тест на создание нового сотрудника"""

        self.client.force_authenticate(user=self.employee)
        data = {
            "username": "newemployee",
            "password": "newpassword",
            "email": "newemployee@example.com",
        }

        response = self.client.post(self.employee_list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get("username"), data["username"])

    def test_get_employee_detail(self):
        """Тест на получение данных сотрудника"""

        self.client.force_authenticate(user=self.employee)

        response = self.client.get(self.employee_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("username"), self.employee.username)

    def test_update_employee(self):
        """Тест на обновление данных сотрудника"""

        self.client.force_authenticate(user=self.employee)

        data = {"username": "updateduser", "email": "updateduser@example.com"}

        response = self.client.patch(self.employee_detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("username"), data["username"])

    def test_delete_employee(self):
        """Тест на удаление данных сотрудника"""

        self.client.force_authenticate(user=self.employee)
        response = self.client.delete(self.employee_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class JWTAuthTestCase(APITestCase):

    def setUp(self):
        """Создание тестового сотрудника для получения токенов"""

        self.password = "jwtpass"
        self.employee = Employee.objects.create_user(
            username="jwtuser", password=self.password
        )
        self.token_url = reverse("employees:token_obtain_pair")
        self.refresh_url = reverse("employees:token_refresh")

    def test_login(self):
        """Тест на получение JWT токена"""

        response = self.client.post(
            self.token_url,
            {"username": self.employee.username, "password": self.password},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("access", data)
        self.assertIn("refresh", data)

    def test_refresh_jwt_token(self):
        """Тест на обновление JWT токена"""

        response = self.client.post(
            self.token_url,
            {"username": self.employee.username, "password": self.password},
            format="json",
        )
        refresh_token = response.json().get("refresh")

        response = self.client.post(
            self.refresh_url, {"refresh": refresh_token}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.json())
