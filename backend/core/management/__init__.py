from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import *
from datetime import date, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Create users
        self.stdout.write('Creating users...')
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@company.com',
            password='admin123',
            is_hr=True
        )

        hr = User.objects.create_user(
            username='hr',
            email='hr@company.com',
            password='hr123',
            is_hr=True,
            is_employee=True
        )

        # Create services
        self.stdout.write('Creating services...')
        services = {
            'IT': Service.objects.create(
                code_service='IT001',
                nom_service='IT Department',
                description='Information Technology',
                email_service='it@company.com'
            ),
            'HR': Service.objects.create(
                code_service='HR001',
                nom_service='Human Resources',
                description='HR Management',
                email_service='hr@company.com'
            )
        }

        # Create employees
        self.stdout.write('Creating employees...')
        employees = []
        for i in range(5):
            emp = Employe.objects.create(
                matricule=f'EMP00{i+1}',
                nom=f'Doe{i+1}',
                prenom=f'John{i+1}',
                date_naissance=date(1990, 1, 1),
                date_embauche=date(2023, 1, 1),
                adresse='123 Street',
                email_pro=f'employee{i+1}@company.com',
                numero_securite_sociale=f'12345{i}',
                situation_familiale='CELIBATAIRE',
                niveau_etudes='MASTER',
                diplome='Computer Science',
                id_service=services['IT'],
                poste_occupe='Developer'
            )
            employees.append(emp)

        # Create contracts
        self.stdout.write('Creating contracts...')
        for emp in employees:
            Contrat.objects.create(
                employe=emp,
                type_contrat='CDI',
                date_debut=emp.date_embauche,
                date_signature=emp.date_embauche,
                salaire_base=50000.00,
                salaire_journalier=2000.00,
                statut='ACTIF'
            )

        # Create leaves
        self.stdout.write('Creating leaves...')
        for emp in employees:
            Conge.objects.create(
                employe=emp,
                date_debut=date.today(),
                date_fin=date.today() + timedelta(days=5),
                type_conge='ANNUEL',
                nb_jours=5,
                justification='Vacances',
                solde_restant=25
            )

        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))