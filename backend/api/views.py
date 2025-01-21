from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Avg, Sum
from datetime import datetime, timedelta
from core.models import *
from core.serializers import *
from .filters import *

class EmployeViewSet(viewsets.ModelViewSet):
    queryset = Employe.objects.all()
    serializer_class = EmployeSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = EmployeFilter
    search_fields = ['nom', 'prenom', 'matricule', 'email_pro']

    @action(detail=False)
    def dashboard(self, request):
        stats = {
            'total': self.queryset.filter(actif=True).count(),
            'by_service': self.queryset.filter(actif=True).values('id_service__nom_service').annotate(count=Count('id_employe')),
            'by_education': self.queryset.filter(actif=True).values('niveau_etudes').annotate(count=Count('id_employe'))
        }
        return Response(stats)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['actif']
    search_fields = ['code_service', 'nom_service']

    @action(detail=True)
    def employees(self, request, pk=None):
        service = self.get_object()
        employees = service.employes.all()
        serializer = EmployeSerializer(employees, many=True)
        return Response(serializer.data)

class ContratViewSet(viewsets.ModelViewSet):
    queryset = Contrat.objects.all()
    serializer_class = ContratSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContratFilter

    @action(detail=False)
    def expiring_soon(self, request):
        thirty_days = datetime.now().date() + timedelta(days=30)
        contracts = self.queryset.filter(
            date_fin__lte=thirty_days,
            archive=False
        )
        serializer = self.get_serializer(contracts, many=True)
        return Response(serializer.data)

class CongeViewSet(viewsets.ModelViewSet):
    queryset = Conge.objects.all()
    serializer_class = CongeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type_conge', 'statut']

    @action(detail=False)
    def pending(self, request):
        leaves = self.queryset.filter(statut='DEMANDE')
        serializer = self.get_serializer(leaves, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def statistics(self, request):
        year = datetime.now().year
        stats = {
            'total_leaves': self.queryset.filter(date_debut__year=year).count(),
            'by_type': self.queryset.filter(date_debut__year=year).values('type_conge').annotate(count=Count('id'))
        }
        return Response(stats)

class SalaireViewSet(viewsets.ModelViewSet):
    queryset = Salaire.objects.all()
    serializer_class = SalaireSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['mois', 'annee', 'employe']

    @action(detail=False, methods=['post'])
    def process_monthly(self, request):
        month = request.data.get('month')
        year = request.data.get('year')
        employees = Employe.objects.filter(actif=True)
        processed = []
        
        for employee in employees:
            contract = Contrat.objects.filter(employe=employee, archive=False).first()
            if contract:
                salary = Salaire.objects.create(
                    employe=employee,
                    contrat=contract,
                    date_paiement=datetime.now().date(),
                    mois=month,
                    annee=year,
                    salaire_base=contract.salaire_base,
                    montant_final=contract.salaire_base,
                    mode_paiement='VIREMENT',
                    statut_paiement='EN_ATTENTE'
                )
                processed.append(self.get_serializer(salary).data)
        return Response(processed)

class MassroufViewSet(viewsets.ModelViewSet):
    queryset = Massrouf.objects.all()
    serializer_class = MassroufSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['statut', 'employe']

class RecrutementViewSet(viewsets.ModelViewSet):
    queryset = Recrutement.objects.all()
    serializer_class = RecrutementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['statut', 'urgent', 'service']
    search_fields = ['titre_poste', 'reference_poste']

    @action(detail=False)
    def statistics(self, request):
        stats = {
            'total_active': self.queryset.filter(statut='OUVERT').count(),
            'by_service': self.queryset.values('service__nom_service').annotate(count=Count('id')),
            'urgent_posts': self.queryset.filter(urgent=True).count()
        }
        return Response(stats)

class CandidatViewSet(viewsets.ModelViewSet):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom', 'prenom', 'email']

class CandidatureViewSet(viewsets.ModelViewSet):
    queryset = Candidature.objects.all()
    serializer_class = CandidatureSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['statut', 'recrutement']

class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['employe', 'date_evaluation']

    @action(detail=False)
    def statistics(self, request):
        stats = {
            'average_score': self.queryset.aggregate(Avg('note_globale')),
            'evaluations_count': self.queryset.count(),
            'by_period': self.queryset.values('periode').annotate(count=Count('id'))
        }
        return Response(stats)

class FormationViewSet(viewsets.ModelViewSet):
    queryset = Formation.objects.all()
    serializer_class = FormationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type_formation', 'statut']

class PointageViewSet(viewsets.ModelViewSet):
    queryset = Pointage.objects.all()
    serializer_class = PointageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['employe', 'date_pointage', 'present']

    @action(detail=False)
    def today(self, request):
        today = datetime.now().date()
        pointages = self.queryset.filter(date_pointage=today)
        serializer = self.get_serializer(pointages, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def statistics(self, request):
        month = datetime.now().month
        year = datetime.now().year
        stats = {
            'present_today': self.queryset.filter(date_pointage=datetime.now().date(), present=True).count(),
            'absent_today': self.queryset.filter(date_pointage=datetime.now().date(), present=False).count(),
            'monthly_hours': self.queryset.filter(
                date_pointage__month=month,
                date_pointage__year=year
            ).aggregate(Sum('heures_travaillees'))
        }
        return Response(stats)

class CompetenceViewSet(viewsets.ModelViewSet):
    queryset = Competence.objects.all()
    serializer_class = CompetenceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom']

    @action(detail=True)
    def employees(self, request, pk=None):
        competence = self.get_object()
        employees = competence.employes.all()
        serializer = EmployeSerializer(employees, many=True)
        return Response(serializer.data)

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['employe', 'type_document']

class HistoriqueViewSet(viewsets.ModelViewSet):
    queryset = Historique.objects.all()
    serializer_class = HistoriqueSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['model_name', 'date_modification']