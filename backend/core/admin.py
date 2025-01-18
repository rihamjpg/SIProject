from django.contrib import admin
from core.models import *

@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'nom', 'prenom', 'email_pro', 'id_service', 'actif')
    list_filter = ('actif', 'id_service', 'niveau_etudes')
    search_fields = ('matricule', 'nom', 'prenom', 'email_pro')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('code_service', 'nom_service', 'id_responsable', 'actif')
    list_filter = ('actif',)
    search_fields = ('code_service', 'nom_service')