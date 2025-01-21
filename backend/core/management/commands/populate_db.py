from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import (
    CustomUser, Employe, Service, Contrat, Conge, Salaire, Massrouf,
    Recrutement, Candidat, Candidature, Evaluation, Formation, Pointage,
    Competence, Favori, Archive, Document, Historique
)
from django.utils import timezone
from datetime import date, timedelta, datetime, time
from django.core.files.base import ContentFile
import random
import string

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with sample data for all models.'

    def handle(self, *args, **options):
        self.stdout.write("Populating database...")
        self.create_users()
        services = self.create_services()
        employees = self.create_employees(services)
        self.create_contracts(employees)
        self.create_leaves(employees)
        self.create_salaries(employees)
        self.create_massrouf(employees)
        recruitments = self.create_recruitments(services)
        candidates = self.create_candidates()
        self.create_candidatures(candidates, recruitments)
        self.create_evaluations(employees)
        self.create_formations(employees)
        self.create_pointages(employees)
        self.create_competences(employees)
        self.create_favoris(employees)
        self.create_archives()
        self.create_documents()
        self.create_historique_entries()
        self.stdout.write(self.style.SUCCESS("Database population complete!"))

    def random_string(self, length=8):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def create_users(self):
        # Superuser
        if not User.objects.filter(email='admin@company.com').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@company.com',
                password='admin123',
                is_hr=True
            )
        # HR user
        if not User.objects.filter(email='hr@company.com').exists():
            User.objects.create_user(
                username='hrmanager',
                email='hr@company.com',
                password='hr123',
                is_hr=True,
                is_employee=True
            )

    def create_services(self):
        service_list = [
            {'code_service': 'IT001', 'nom_service': 'IT Department'},
            {'code_service': 'HR001', 'nom_service': 'Human Resources'},
            {'code_service': 'FIN001', 'nom_service': 'Finance'},
            {'code_service': 'MKT001', 'nom_service': 'Marketing'}
        ]
        services = []
        for s in service_list:
            obj, _ = Service.objects.get_or_create(
                code_service=s['code_service'],
                defaults={
                    'nom_service': s['nom_service'],
                    'description': f"Dept of {s['nom_service']}",
                    'localisation': 'Head Office',
                    'telephone': f'+213555{random.randint(1000,9999)}'
                }
            )
            services.append(obj)
        return services

    def create_employees(self, services):
        employees = []
        # Create 10 employees
        for i in range(10):
            service = random.choice(services)
            mat = f"EMP{i+1:03d}"
            employe, _ = Employe.objects.get_or_create(
                matricule=mat,
                defaults={
                    'nom': f"Nom{i+1}",
                    'prenom': f"Prenom{i+1}",
                    'date_naissance': date(1985 + i, 1, 1) + timedelta(days=i*5),
                    'date_embauche': date(2020, 1, 1) + timedelta(days=i*30),
                    'adresse': f"Addresse{i+1}",
                    'telephone_mobile': f"+213765{i:04d}",
                    'email_pro': f"emp{i+1}@company.com",
                    'email_perso': f"emp{i+1}@personal.com",
                    'numero_securite_sociale': f"SSN{i+1:06d}",
                    'situation_familiale': random.choice(
                        [x[0] for x in Employe.SITUATION_FAMILIALE_CHOICES]
                    ),
                    'niveau_etudes': random.choice(
                        [x[0] for x in Employe.NIVEAU_ETUDES_CHOICES]
                    ),
                    'diplome': f"Diplome{i+1}",
                    'id_service': service,
                    'poste_occupe': f"Poste{i+1}",
                    'nombre_enfants': random.randint(0, 3),
                }
            )
            employees.append(employe)
        return employees

    def create_contracts(self, employees):
        for emp in employees:
            Contrat.objects.get_or_create(
                employe=emp,
                type_contrat=random.choice(['CDI', 'CDD', 'STAGE', 'APPRENTISSAGE']),
                date_debut=emp.date_embauche,
                date_signature=emp.date_embauche,
                salaire_base=random.randint(40000, 120000),
                salaire_journalier=random.randint(1500, 6000),
                statut='Actif'
            )

    def create_leaves(self, employees):
        for i, emp in enumerate(employees):
            date_start = date.today() + timedelta(days=i+1)
            Conge.objects.get_or_create(
                employe=emp,
                date_debut=date_start,
                date_fin=date_start + timedelta(days=5),
                type_conge=random.choice([x[0] for x in Conge.TYPE_CONGE_CHOICES]),
                nb_jours=5,
                justification="Vacances annuelles",
                solde_restant=20 - (i if i < 20 else 5),
                defaults={
                    'statut': 'DEMANDE'
                }
            )

    def create_salaries(self, employees):
        for emp in employees:
            mois = random.randint(1, 12)
            annee = 2023
            base = random.randint(40000, 120000)
            heures_sup = random.randint(0, 10)
            Salaire.objects.get_or_create(
                employe=emp,
                contrat=emp.contrat_set.first(),
                date_paiement=date(annee, mois, 25),
                salaire_base=base,
                heures_supplementaires=heures_sup,
                prime_rendement=random.randint(0, 5000),
                prime_anciennete=random.randint(0, 3000),
                taux_horaire_sup=200,
                indemnites=2000,
                avance_salaire=0,
                montant_final=base + 2000 + (heures_sup * 200),
                mois=mois,
                annee=annee,
                mode_paiement="Virement Bancaire",
                reference_paiement=f"PAY-{annee}{mois}{emp.matricule}",
                statut_paiement="Payé",
            )

    def create_massrouf(self, employees):
        for emp in employees:
            Massrouf.objects.get_or_create(
                employe=emp,
                montant_demande=random.randint(2000, 20000),
                statut=random.choice(['EN_ATTENTE', 'APPROUVÉ', 'REJETÉ'])
            )

    def create_recruitments(self, services):
        recs = []
        for i in range(3):
            service = random.choice(services)
            ref = f"REC{i+1:03d}"
            r, _ = Recrutement.objects.get_or_create(
                reference_poste=ref,
                defaults={
                    'titre_poste': f"Poste {i+1}",
                    'description_poste': "Description de poste",
                    'competences_requises': "Compétences diverses",
                    'experience_requise': "2 ans minimum",
                    'niveau_etudes_requis': "Licence",
                    'date_publication': date(2023, 1, 1) + timedelta(days=i*10),
                    'date_cloture': date(2023, 1, 20) + timedelta(days=i*10),
                    'statut': random.choice([x[0] for x in Recrutement.STATUT_CHOICES]),
                    'postes_disponibles': random.randint(1, 5),
                    'salaire_propose': random.randint(30000, 80000),
                    'type_contrat_propose': random.choice(['CDI', 'CDD', 'STAGE']),
                    'service': service,
                    'localisation_poste': f"Localisation {i+1}",
                    'urgent': bool(random.getrandbits(1))
                }
            )
            recs.append(r)
        return recs

    def create_candidates(self):
        candidates = []
        for i in range(5):
            email = f"candidate{i+1}@mail.com"
            c, _ = Candidat.objects.get_or_create(
                email=email,
                defaults={
                    'nom': f"CandidatNom{i+1}",
                    'prenom': f"CandidatPrenom{i+1}",
                    'mot_de_passe': self.random_string(12),
                    'telephone': f"+213557{i:04d}",
                    'source_recrutement': "LinkedIn"
                }
            )
            candidates.append(c)
        return candidates

    def create_applications(self, candidates, recruitments):
        for c in candidates:
            rec = random.choice(recruitments)
            Candidature.objects.get_or_create(
                candidat=c,
                recrutement=rec,
                defaults={
                    'statut': "En cours",
                    'notes_recruteur': "Notes initiales"
                }
            )

    def create_evaluations(self, employees):
        for i, emp in enumerate(employees):
            # Random date
            date_eval = date(2022, 1, 1) + timedelta(days=i*10)
            # Evaluateur random
            evaluateur = random.choice(employees)
            if evaluateur == emp:
                evaluateur = random.choice(employees)
            Evaluation.objects.get_or_create(
                employe=emp,
                evaluateur=evaluateur,
                date_evaluation=date_eval,
                defaults={
                    'note_globale': random.uniform(0, 20),
                    'commentaires': "Bon travail global",
                    'periode': "Annuel",
                    'objectifs_fixes': "Augmenter la productivité",
                    'objectifs_atteints': "Objectifs partiellement atteints",
                    'axes_amelioration': "Communication, Organisation",
                    'besoins_formation': "Formation en management",
                    'entretien_realise': True,
                    'date_prochaine_evaluation': date_eval + timedelta(days=180)
                }
            )

    def create_formations(self, employees):
        for i in range(3):
            formateur = random.choice(employees)
            Formation.objects.get_or_create(
                titre=f"Formation {i+1}",
                formateur=formateur,
                date_debut=date(2023, 5, 1) + timedelta(days=i*10),
                date_fin=date(2023, 5, 5) + timedelta(days=i*10),
                cout=random.randint(10000, 50000),
                duree_heures=30 + i*5,
                type_formation="Soft Skills",
                niveau="Débutant",
                places_disponibles=20,
                statut="Planifiée",
                objectifs="Améliorer les compétences",
                prerequis="Aucun",
                lieu="Centre de formation"
            )

    def create_pointages(self, employees):
        today = date.today()
        for emp in employees:
            for day_offset in range(5):
                date_p = today - timedelta(days=day_offset)
                arrival = time(9, 0)
                departure = time(17, 0)
                try:
                    Pointage.objects.get_or_create(
                        employe=emp,
                        date_pointage=date_p,
                        defaults={
                            'heure_arrivee': arrival,
                            'heure_depart': departure,
                            'present': True,
                            'heures_travaillees': 8.0,
                            'heures_supplementaires': 0,
                        }
                    )
                except:
                    pass

    def create_competences(self, employees):
        for c_name in ['Python', 'Django', 'React', 'Angular', 'Machine Learning']:
            comp, _ = Competence.objects.get_or_create(nom=c_name)
            emp_sample = random.sample(employees, k=min(len(employees), 3))
            for emp in emp_sample:
                comp.employes.add(emp)

    def create_favoris(self, employees):
        for emp in employees:
            Favori.objects.get_or_create(
                employe=emp,
                nom_fonctionnalite="Dashboard",
                defaults={'position_ordre': 1}
            )

    def create_archives(self):
        Archive.objects.get_or_create(
            nom_archive="Archive 2023",
            defaults={
                'description': "Archive des données de l'année 2023",
                'contenu': {'key': 'value'}
            }
        )

    def create_documents(self):
            # Create example documents for each employee
            employees = Employe.objects.all()
            for i, emp in enumerate(employees):
                Document.objects.create(
                    employe=emp,
                    type_document='Attestation',
                    nom_fichier=f'attestation_{emp.matricule}.pdf',
                    description='Attestation de travail',
                    confidentialite='PRIVE'
                )
                Document.objects.create(
                    employe=emp,
                    type_document='Certificat',
                    nom_fichier=f'certificat_{emp.matricule}.pdf',
                    description='Certificat divers',
                    confidentialite='CONFIDENTIEL'
                )
            self.stdout.write('Created documents for employees.')
    def create_historique_entries(self):
        """
        Create some sample historique entries to simulate model changes.
        """
        # We'll log changes for some random employees
        employees = Employe.objects.all()
        for i, emp in enumerate(employees):
            Historique.objects.create(
                model_name='Employe',
                instance_id=emp.id_employe,
                utilisateur='admin@company.com',
                modifications={
                    'poste_occupe': f"Ancien Poste{i+1} -> {emp.poste_occupe}",
                    'service': str(emp.id_service)
                }
            )
    def create_candidatures(self, candidates, recruitments):
        """
        Assign random recruitments to each candidate for demonstration.
        """
        for candidate in candidates:
            recrutement = random.choice(recruitments)
            Candidature.objects.get_or_create(
                candidat=candidate,
                recrutement=recrutement,
                defaults={
                    'statut': 'En cours',
                    'notes_recruteur': 'Initial notes',
                    'evaluation_entretien': '',
                    'decision_finale': '',
                }
            )