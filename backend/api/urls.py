from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmployeeViewSet, ServiceViewSet, ContractViewSet,
    LeaveViewSet, SalaryViewSet, PointageViewSet,
    RecruitmentViewSet
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .auth import register_user, candidate_register

# Create router and register viewsets
router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'contracts', ContractViewSet)
router.register(r'leaves', LeaveViewSet)
router.register(r'salaries', SalaryViewSet)
router.register(r'pointages', PointageViewSet)
router.register(r'recruitments', RecruitmentViewSet)

urlpatterns = [
    # API Routes
    path('', include(router.urls)),
    
    # Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register_user, name='register'),
    path('register/candidate/', candidate_register, name='candidate_register'),
    
    # Analytics Routes
    path('analytics/dashboard/', EmployeeViewSet.as_view({'get': 'dashboard'}), name='dashboard'),
    path('analytics/absences/', EmployeeViewSet.as_view({'get': 'absence_report'}), name='absence-report'),
    path('analytics/recruitment/', RecruitmentViewSet.as_view({'get': 'recruitment_stats'}), name='recruitment-stats'),
    
    # Employee Related Routes
    path('employees/<int:pk>/contracts/', ContractViewSet.as_view({'get': 'employee_contracts'}), name='employee-contracts'),
    path('employees/<int:pk>/leaves/', LeaveViewSet.as_view({'get': 'employee_leaves'}), name='employee-leaves'),
    path('employees/<int:pk>/salary-history/', SalaryViewSet.as_view({'get': 'employee_salary_history'}), name='employee-salary-history'),
    
    # Batch Operations
    path('payroll/process-monthly/', SalaryViewSet.as_view({'post': 'process_monthly_payroll'}), name='process-monthly-payroll'),
    path('contracts/expiring-soon/', ContractViewSet.as_view({'get': 'expiring_soon'}), name='contracts-expiring-soon'),
]