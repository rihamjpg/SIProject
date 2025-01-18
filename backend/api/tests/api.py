from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.models import CustomUser, Employee, Service

class EmployeeViewSetTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_superuser(
            email='admin@test.com',
            username='admin',
            password='admin123'
        )
        self.client.force_authenticate(user=self.user)
        self.service = Service.objects.create(
            code='IT',
            description='Information Technology'
        )

    def test_create_employee(self):
        url = reverse('employee-list')
        data = {
            'code': 'EMP001',
            'nom': 'Doe',
            'prenom': 'John',
            'service': self.service.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_employees(self):
        url = reverse('employee-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)