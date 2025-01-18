from django.test import TestCase
from django.utils import timezone
from core.models import CustomUser, Employee, Service, Contract, Leave, Salary

class ServiceTests(TestCase):
    def test_create_service(self):
        service = Service.objects.create(
            code='IT',
            description='Information Technology'
        )
        self.assertEqual(str(service), 'IT - Information Technology')

class EmployeeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.service = Service.objects.create(
            code='IT',
            description='Information Technology'
        )

    def test_create_employee(self):
        employee = Employee.objects.create(
            code='EMP001',
            nom='Doe',
            prenom='John',
            date_naissance='1990-01-01',
            date_embauche='2020-01-01',
            adresse='123 Test St',
            service=self.service,
            email='john@example.com',
            telephone='1234567890'
        )
        self.assertEqual(str(employee), 'EMP001 - John Doe')

class ContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        service = Service.objects.create(code='IT', description='IT')
        cls.employee = Employee.objects.create(
            code='EMP001',
            nom='Doe',
            service=service
        )

    def test_create_contract(self):
        contract = Contract.objects.create(
            employe=self.employee,
            type_contrat='CDI',
            date_debut='2023-01-01',
            salaire_mensuel=5000,
            salaire_journalier=250
        )
        self.assertEqual(contract.type_contrat, 'CDI')