from rest_framework import serializers
from .models import (
    Employe, Service, Contrat, Conge, Salaire, 
    Massrouf, Recrutement, Candidat, Candidature,
    Evaluation, Formation, Pointage, Competence,
    Favori, Archive, Document, Historique
)
from django.contrib.auth import get_user_model


class ServiceSerializer(serializers.ModelSerializer):
    responsable_name = serializers.CharField(source='id_responsable.nom', read_only=True)
    
    class Meta:
        model = Service
        fields = '__all__'

class EmployeSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='id_service.nom_service', read_only=True)
    competences = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Employe
        fields = '__all__'
        extra_kwargs = {
            'piece_identite': {'required': False},
            'photo': {'required': False},
        }

class ContratSerializer(serializers.ModelSerializer):
    employe_name = serializers.CharField(source='employe.nom', read_only=True)
    
    class Meta:
        model = Contrat
        fields = '__all__'

class CongeSerializer(serializers.ModelSerializer):
    employe_name = serializers.CharField(source='employe.nom', read_only=True)
    valideur_name = serializers.CharField(source='valideur.nom', read_only=True)
    
    class Meta:
        model = Conge
        fields = '__all__'

class SalaireSerializer(serializers.ModelSerializer):
    employe_name = serializers.CharField(source='employe.nom', read_only=True)
    
    class Meta:
        model = Salaire
        fields = '__all__'

class MassroufSerializer(serializers.ModelSerializer):
    employe_name = serializers.CharField(source='employe.nom', read_only=True)
    
    class Meta:
        model = Massrouf
        fields = '__all__'

class RecrutementSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.nom_service', read_only=True)
    
    class Meta:
        model = Recrutement
        fields = '__all__'

class CandidatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidat
        fields = '__all__'
        extra_kwargs = {
            'mot_de_passe': {'write_only': True},
            'code_confirmation': {'write_only': True}
        }

class CandidatureSerializer(serializers.ModelSerializer):
    candidat_name = serializers.CharField(source='candidat.nom', read_only=True)
    poste = serializers.CharField(source='recrutement.titre_poste', read_only=True)
    
    class Meta:
        model = Candidature
        fields = '__all__'

class EvaluationSerializer(serializers.ModelSerializer):
    employe_name = serializers.CharField(source='employe.nom', read_only=True)
    evaluateur_name = serializers.CharField(source='evaluateur.nom', read_only=True)
    
    class Meta:
        model = Evaluation
        fields = '__all__'

class FormationSerializer(serializers.ModelSerializer):
    formateur_name = serializers.CharField(source='formateur.nom', read_only=True)
    
    class Meta:
        model = Formation
        fields = '__all__'

class PointageSerializer(serializers.ModelSerializer):
    employe_name = serializers.CharField(source='employe.nom', read_only=True)
    validateur_name = serializers.CharField(source='validateur.nom', read_only=True)
    
    class Meta:
        model = Pointage
        fields = '__all__'

class CompetenceSerializer(serializers.ModelSerializer):
    employes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Competence
        fields = '__all__'
        
    def get_employes_count(self, obj):
        return obj.employes.count()

class FavoriSerializer(serializers.ModelSerializer):
    employe_name = serializers.CharField(source='employe.nom', read_only=True)
    
    class Meta:
        model = Favori
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    employe_name = serializers.CharField(source='employe.nom', read_only=True)
    
    class Meta:
        model = Document
        fields = '__all__'

class HistoriqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historique
        fields = '__all__'

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'is_employee', 'is_hr', 'is_manager')
        extra_kwargs = {
            'password': {'write_only': True},
            'is_hr': {'read_only': True},
            'is_manager': {'read_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user