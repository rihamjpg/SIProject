from rest_framework import serializers 
from .models import Employee, Service, Contract, Leave, Salary, Pointage, Recruitment
from django.contrib.auth import get_user_model

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'code', 'description']

class EmployeeSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.description', read_only=True)
    
    class Meta:
        model = Employee
        fields = ['id', 'code', 'nom', 'prenom', 'date_naissance', 
                 'date_embauche', 'adresse', 'service', 'service_name',
                 'email', 'telephone']

class ContractSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employe.nom', read_only=True)
    
    class Meta:
        model = Contract
        fields = ['id', 'employe', 'employee_name', 'type_contrat', 
                 'date_debut', 'date_fin', 'salaire_mensuel',
                 'salaire_journalier', 'archive']

class LeaveSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employe.nom', read_only=True)
    
    class Meta:
        model = Leave
        fields = ['id', 'employe', 'employee_name', 'type_conge',
                 'date_debut', 'date_fin', 'nb_jours',
                 'justification', 'statut']

class SalarySerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employe.nom', read_only=True)
    
    class Meta:
        model = Salary
        fields = ['id', 'employe', 'employee_name', 'mois', 'annee',
                 'salaire_base', 'primes', 'avance_salaire',
                 'total_net', 'date_paiement']

class PointageSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employe.nom', read_only=True)
    
    class Meta:
        model = Pointage
        fields = ['id', 'employe', 'employee_name', 'date_pointage',
                 'present', 'conge']

class RecruitmentSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.description', read_only=True)
    
    class Meta:
        model = Recruitment
        fields = ['id', 'titre', 'description', 'type_contrat',
                 'service', 'service_name', 'date_publication', 'statut']

class EmployeeDetailSerializer(EmployeeSerializer):
    contracts = ContractSerializer(many=True, read_only=True, source='contract_set')
    leaves = LeaveSerializer(many=True, read_only=True, source='leave_set')
    salaries = SalarySerializer(many=True, read_only=True, source='salary_set')
    
    class Meta(EmployeeSerializer.Meta):
        fields = EmployeeSerializer.Meta.fields + ['contracts', 'leaves', 'salaries']

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 
                 'is_employee', 'is_hr', 'is_manager',
                 'verification_token')
        read_only_fields = ('verification_token',)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user