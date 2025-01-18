from django.db import models
from django.contrib.auth.models import AbstractUser


class Service(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField()

class Employee(models.Model):
    code = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    date_embauche = models.DateField()
    adresse = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)
    
class Contract(models.Model):
    TYPE_CHOICES = [
        ('CDI', 'Contrat à Durée Indéterminée'),
        ('CDD', 'Contrat à Durée Déterminée'),
        ('STAGE', 'Stage'),
    ]
    
    employe = models.ForeignKey(Employee, on_delete=models.CASCADE)
    type_contrat = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    salaire_mensuel = models.DecimalField(max_digits=10, decimal_places=2)
    salaire_journalier = models.DecimalField(max_digits=10, decimal_places=2)
    archive = models.BooleanField(default=False)

class Leave(models.Model):
    TYPE_CHOICES = [
        ('ANNUEL', 'Congé Annuel'),
        ('MALADIE', 'Congé Maladie'),
        ('MATERNITE', 'Congé Maternité'),
        ('PATERNITE', 'Congé Paternité'),
        ('SANS_SOLDE', 'Congé Sans Solde'),
    ]
    
    STATUS_CHOICES = [
        ('DEMANDE', 'Demandé'),
        ('APPROUVE', 'Approuvé'),
        ('REFUSE', 'Refusé'),
    ]
    
    employe = models.ForeignKey(Employee, on_delete=models.CASCADE)
    type_conge = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_debut = models.DateField()
    date_fin = models.DateField()
    nb_jours = models.IntegerField()
    justification = models.TextField(blank=True)
    statut = models.CharField(max_length=10, choices=STATUS_CHOICES)

class Salary(models.Model):
    employe = models.ForeignKey(Employee, on_delete=models.CASCADE)
    mois = models.IntegerField()
    annee = models.IntegerField()
    salaire_base = models.DecimalField(max_digits=10, decimal_places=2)
    primes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    avance_salaire = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_net = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField(auto_now_add=True)

class Pointage(models.Model):
    employe = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date_pointage = models.DateField()
    present = models.BooleanField(default=True)
    conge = models.BooleanField(default=False)

class Recruitment(models.Model):
    STATUS_CHOICES = [
        ('PUBLIE', 'Publié'),
        ('EN_COURS', 'En Cours'),
        ('TERMINE', 'Terminé'),
    ]
    
    titre = models.CharField(max_length=200)
    description = models.TextField()
    type_contrat = models.CharField(max_length=10, choices=Contract.TYPE_CHOICES)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_publication = models.DateField(auto_now_add=True)
    statut = models.CharField(max_length=10, choices=STATUS_CHOICES)



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_employee = models.BooleanField(default=False)
    is_hr = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']