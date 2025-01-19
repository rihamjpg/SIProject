from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import *
from datetime import date, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting database population...')

        try:
            # Create superuser
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@company.com',
                password='admin123',
                is_hr=True
            )
            self.stdout.write('Created admin user')

            # Create HR Manager
            hr_manager = User.objects.create_user(
                username='hrmanager',
                email='hr@company.com',
                password='hr123',
                is_hr=True,
                is_employee=True
            )
            self.stdout.write('Created HR manager')

            # Create Services
            services = {
                'IT': Service.objects.create(
                    code_service='IT001',
                    nom_service='IT Department',
                    description='Information Technology',
                    email_service='it@company.com',
                    localisation='Building A'
                ),
                'HR': Service.objects.create(
                    code_service='HR001',
                    nom_service='Human Resources',
                    description='HR Department',
                    email_service='hr@company.com',
                    localisation='Building B'
                ),
                'FIN': Service.objects.create(
                    code_service='FIN001',
                    nom_service='Finance',
                    description='Finance Department',
                    email_service='finance@company.com',
                    localisation='Building C'
                )
            }
            self.stdout.write('Created services')

            # Create Employees
            for i in range(10):
                service = random.choice(list(services.values()))
                emp = Employe.objects.create(
                    matricule=f'EMP{i+1:03d}',
                    nom=f'LastName{i+1}',
                    prenom=f'FirstName{i+1}',
                    date_naissance=date(1990 + i % 10, (i % 12) + 1, (i % 28) + 1),
                    date_embauche=date(2023, (i % 12) + 1, (i % 28) + 1),
                    adresse=f'Address {i+1}',
                    telephone_mobile=f'+213555{i:05d}',
                    email_pro=f'employee{i+1}@company.com',
                    email_perso=f'personal{i+1}@email.com',
                    numero_securite_sociale=f'SSN{i+1:05d}',
                    situation_familiale=random.choice(['CELIBATAIRE', 'MARIE']),
                    niveau_etudes=random.choice(['LICENCE', 'MASTER', 'DOCTORAT']),
                    diplome=f'Degree {i+1}',
                    id_service=service,
                    poste_occupe=f'Position {i+1}'
                )

                # Create Contract
                Contrat.objects.create(
                    employe=emp,
                    type_contrat='CDI',
                    date_debut=emp.date_embauche,
                    date_signature=emp.date_embauche,
                    salaire_base=random.randint(50000, 100000),
                    salaire_journalier=random.randint(2000, 4000),
                    statut='ACTIF'
                )

                # Create Leave
                Conge.objects.create(
                    employe=emp,
                    date_debut=date.today() + timedelta(days=i*7),
                    date_fin=date.today() + timedelta(days=(i*7)+5),
                    type_conge='ANNUEL',
                    statut='DEMANDE',
                    nb_jours=5,
                    justification='Congés annuels',
                    solde_restant=25
                )

            self.stdout.write(self.style.SUCCESS('Database populated successfully!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))