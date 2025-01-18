from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta, timezone
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from core.services import calculate_salary, manage_leave, generate_report
from core.models import *
from core.serializers import *


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
    @action(detail=True, methods=['get'])
    def salary_calculation(self, request, pk=None):
        month = int(request.query_params.get('month', datetime.now().month))
        year = int(request.query_params.get('year', datetime.now().year))
        
        salary_data = calculate_salary(pk, month, year)
        if salary_data:
            return Response(salary_data)
        return Response({'error': 'Cannot calculate salary'}, status=status.HTTP_400_BAD_REQUEST)
    
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'description']

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type_contrat', 'archive']
    search_fields = ['employe__nom']

    @action(detail=False, methods=['get'])
    def expiring_soon(self, request):
        """Get contracts expiring in the next 30 days"""
        thirty_days = timezone.now().date() + timedelta(days=30)
        contracts = Contract.objects.filter(
            date_fin__lte=thirty_days,
            archive=False
        )
        serializer = self.get_serializer(contracts, many=True)
        return Response(serializer.data)

# class SalaryViewSet(viewsets.ModelViewSet):
#     queryset = Salary.objects.all()
#     serializer_class = SalarySerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['mois', 'annee']

#     @action(detail=False, methods=['post'])
#     def process_monthly_payroll(self, request):
#         """Process payroll for all employees"""
#         month = request.data.get('month')
#         year = request.data.get('year')
#         employees = Employee.objects.all()
#         results = []
        
#         for employee in employees:
#             salary_data = calculate_salary(employee.id, month, year)
#             if salary_data:
#                 salary = Salary.objects.create(
#                     employe=employee,
#                     mois=month,
#                     annee=year,
#                     **salary_data
#                 )
#                 results.append(self.get_serializer(salary).data)
        
#         return Response(results)


class LeaveViewSet(viewsets.ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type_conge', 'statut']
    search_fields = ['employe__nom']

    @action(detail=False)
    def pending_approvals(self, request):
        leaves = self.queryset.filter(statut='DEMANDE')
        serializer = self.get_serializer(leaves, many=True)
        return Response(serializer.data)

class SalaryViewSet(viewsets.ModelViewSet):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['mois', 'annee']

    @action(detail=False, methods=['post'])
    def process_monthly(self, request):
        month = request.data.get('month')
        year = request.data.get('year')
        processed = []
        
        for employee in Employee.objects.all():
            salary_data = calculate_salary(employee.id, month, year)
            if salary_data:
                salary = Salary.objects.create(
                    employe=employee,
                    mois=month,
                    annee=year,
                    **salary_data
                )
                processed.append(self.get_serializer(salary).data)
        return Response(processed)

class PointageViewSet(viewsets.ModelViewSet):
    queryset = Pointage.objects.all()
    serializer_class = PointageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date_pointage', 'present']

    @action(detail=False)
    def absences_today(self, request):
        today = datetime.now().date()
        absences = self.queryset.filter(date_pointage=today, present=False)
        serializer = self.get_serializer(absences, many=True)
        return Response(serializer.data)

class RecruitmentViewSet(viewsets.ModelViewSet):
    queryset = Recruitment.objects.all()
    serializer_class = RecruitmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['statut', 'type_contrat']
    search_fields = ['titre', 'description']

    @action(detail=False)
    def active_positions(self, request):
        positions = self.queryset.filter(statut='PUBLIE')
        serializer = self.get_serializer(positions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        recruitment = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(Recruitment.STATUS_CHOICES):
            recruitment.statut = new_status
            recruitment.save()
            return Response(self.get_serializer(recruitment).data)
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)