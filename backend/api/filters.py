import django_filters
from core.models import *

class EmployeFilter(django_filters.FilterSet):
    date_embauche_min = django_filters.DateFilter(field_name='date_embauche', lookup_expr='gte')
    date_embauche_max = django_filters.DateFilter(field_name='date_embauche', lookup_expr='lte')
    service = django_filters.CharFilter(field_name='id_service__nom_service', lookup_expr='icontains')
    
    class Meta:
        model = Employe
        fields = {
            'actif': ['exact'],
            'niveau_etudes': ['exact'],
            'situation_familiale': ['exact'],
            'poste_occupe': ['exact', 'icontains']
        }

class ServiceFilter(django_filters.FilterSet):
    responsable = django_filters.CharFilter(field_name='id_responsable__nom', lookup_expr='icontains')
    
    class Meta:
        model = Service
        fields = {
            'actif': ['exact'],
            'code_service': ['exact', 'icontains'],
            'localisation': ['exact', 'icontains']
        }

class ContratFilter(django_filters.FilterSet):
    date_debut_min = django_filters.DateFilter(field_name='date_debut', lookup_expr='gte')
    date_fin_max = django_filters.DateFilter(field_name='date_fin', lookup_expr='lte')
    salaire_min = django_filters.NumberFilter(field_name='salaire_base', lookup_expr='gte')
    salaire_max = django_filters.NumberFilter(field_name='salaire_base', lookup_expr='lte')
    
    class Meta:
        model = Contrat
        fields = {
            'type_contrat': ['exact'],
            'archive': ['exact'],
            'periode_essai': ['exact']
        }

class CongeFilter(django_filters.FilterSet):
    date_debut_min = django_filters.DateFilter(field_name='date_debut', lookup_expr='gte')
    date_fin_max = django_filters.DateFilter(field_name='date_fin', lookup_expr='lte')
    
    class Meta:
        model = Conge
        fields = {
            'type_conge': ['exact'],
            'statut': ['exact'],
            'employe': ['exact'],
            'solde_deductible': ['exact']
        }

class SalaireFilter(django_filters.FilterSet):
    montant_min = django_filters.NumberFilter(field_name='montant_final', lookup_expr='gte')
    montant_max = django_filters.NumberFilter(field_name='montant_final', lookup_expr='lte')
    
    class Meta:
        model = Salaire
        fields = {
            'mois': ['exact'],
            'annee': ['exact'],
            'mode_paiement': ['exact'],
            'statut_paiement': ['exact']
        }

class RecrutementFilter(django_filters.FilterSet):
    salaire_min = django_filters.NumberFilter(field_name='salaire_propose', lookup_expr='gte')
    date_publication_min = django_filters.DateFilter(field_name='date_publication', lookup_expr='gte')
    
    class Meta:
        model = Recrutement
        fields = {
            'statut': ['exact'],
            'urgent': ['exact'],
            'service': ['exact'],
            'type_contrat_propose': ['exact']
        }

class PointageFilter(django_filters.FilterSet):
    date_min = django_filters.DateFilter(field_name='date_pointage', lookup_expr='gte')
    date_max = django_filters.DateFilter(field_name='date_pointage', lookup_expr='lte')
    
    class Meta:
        model = Pointage
        fields = {
            'employe': ['exact'],
            'present': ['exact'],
            'conge': ['exact'],
            'jour_ferie': ['exact']
        }