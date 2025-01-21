from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmployeViewSet, ServiceViewSet, ContratViewSet,
    CongeViewSet, SalaireViewSet, PointageViewSet,
    RecrutementViewSet, CandidatViewSet, CandidatureViewSet,
    EvaluationViewSet, FormationViewSet, CompetenceViewSet,
    DocumentViewSet, HistoriqueViewSet, MassroufViewSet
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .auth import register_user, candidate_register, login
from django.conf.urls.static import static
from django.conf import settings

# Create router and register viewsets
router = DefaultRouter()
router.register(r'employees', EmployeViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'contracts', ContratViewSet)
router.register(r'leaves', CongeViewSet)
router.register(r'salaries', SalaireViewSet)
router.register(r'pointages', PointageViewSet)
router.register(r'recruitments', RecrutementViewSet)
router.register(r'candidates', CandidatViewSet)
router.register(r'applications', CandidatureViewSet)
router.register(r'evaluations', EvaluationViewSet)
router.register(r'trainings', FormationViewSet)
router.register(r'skills', CompetenceViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'history', HistoriqueViewSet)
router.register(r'massroufs', MassroufViewSet)

urlpatterns = [
    # API Routes
    path('', include(router.urls)),
    
    # Authentication
    path('register/', register_user, name='register'),
    path('register/candidate/', candidate_register, name='candidate_register'),
    path('login/', login, name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Analytics Routes
    path('analytics/dashboard/', EmployeViewSet.as_view({'get': 'dashboard'}), name='dashboard'),
    path('analytics/absences/', CongeViewSet.as_view({'get': 'absence_report'}), name='absence-report'),
    path('analytics/recruitment/', RecrutementViewSet.as_view({'get': 'recruitment_stats'}), name='recruitment-stats'),
    path('analytics/salaries/', SalaireViewSet.as_view({'get': 'process_monthly'}), name='salary-stats'),
    
    # Custom Actions
    path('contracts/expiring/', ContratViewSet.as_view({'get': 'expiring_soon'}), name='expiring-contracts'),
    path('leaves/pending/', CongeViewSet.as_view({'get': 'pending'}), name='pending-leaves'),
    path('pointages/today/', PointageViewSet.as_view({'get': 'today'}), name='today-attendance'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)