from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Sum
from .models import Employee, Contract, Salary, Leave, Pointage

def get_employee_data(employee_id):
    """Get complete employee data including related information"""
    try:
        employee = Employee.objects.get(id_employe=employee_id)
        contracts = Contract.objects.filter(employe=employee)
        leaves = Leave.objects.filter(employe=employee)
        salary_history = Salary.objects.filter(employe=employee)
        
        return {
            'employee': employee,
            'contracts': contracts,
            'leaves': leaves,
            'salary_history': salary_history
        }
    except Employee.DoesNotExist:
        return None

def calculate_salary(employee_id, month, year):
    """Calculate employee salary for given month including deductions"""
    try:
        employee = Employee.objects.get(id_employe=employee_id)
        contract = Contract.objects.filter(employe=employee, archive=False).first()
        
        if not contract:
            return None
            
        # Get all absences for the month
        start_date = datetime(year, month, 1)
        end_date = start_date.replace(day=1) + timedelta(days=32)
        end_date = end_date.replace(day=1) - timedelta(days=1)
        
        absences = Pointage.objects.filter(
            employe=employee,
            date_pointage__range=(start_date, end_date),
            present=False,
            conge=False
        ).count()
        
        # Calculate base salary
        daily_salary = contract.salaire_journalier
        working_days = 22  # Approximate working days per month
        base_salary = daily_salary * (working_days - absences)
        
        # Get advances
        advances = Salary.objects.filter(
            employe=employee,
            mois=month,
            annee=year
        ).aggregate(Sum('avance_salaire'))['avance_salaire__sum'] or 0
        
        # Final salary calculation
        final_salary = base_salary - Decimal(advances)
        
        return {
            'base_salary': base_salary,
            'absences': absences,
            'deductions': advances,
            'final_salary': final_salary
        }
    except Employee.DoesNotExist:
        return None

def manage_leave(employee_id, leave_data):
    """Process leave requests"""
    try:
        employee = Employee.objects.get(id_employe=employee_id)
        
        # Check remaining leave balance
        total_leaves = Leave.objects.filter(
            employe=employee,
            type_conge=leave_data['type_conge'],
            statut='APPROUVE'
        ).aggregate(Sum('nb_jours'))['nb_jours__sum'] or 0
        
        if leave_data['type_conge'] == 'ANNUEL' and total_leaves + leave_data['nb_jours'] > 30:
            return {'status': 'error', 'message': 'Solde de congés insuffisant'}
            
        # Create leave request
        leave = Leave.objects.create(
            employe=employee,
            date_debut=leave_data['date_debut'],
            date_fin=leave_data['date_fin'],
            type_conge=leave_data['type_conge'],
            nb_jours=leave_data['nb_jours'],
            justification=leave_data.get('justification', ''),
            statut='DEMANDE'
        )
        
        return {'status': 'success', 'leave': leave}
    except Employee.DoesNotExist:
        return {'status': 'error', 'message': 'Employé non trouvé'}

def generate_report(report_type, start_date, end_date):
    """Generate HR reports based on type and date range"""
    if report_type == 'absences':
        return Pointage.objects.filter(
            date_pointage__range=(start_date, end_date),
            present=False
        ).values('employe__nom', 'employe__prenom', 'date_pointage')
        
    elif report_type == 'new_hires':
        return Employee.objects.filter(
            date_embauche__range=(start_date, end_date)
        ).values('nom', 'prenom', 'date_embauche', 'poste_occupe')
        
    elif report_type == 'contracts_ending':
        return Contract.objects.filter(
            date_fin__range=(start_date, end_date),
            archive=False
        ).values('employe__nom', 'employe__prenom', 'type_contrat', 'date_fin')
    
    return None