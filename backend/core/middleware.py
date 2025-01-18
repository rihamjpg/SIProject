from django.utils import timezone
from .models import Historique

class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated and request.method not in ['GET', 'HEAD', 'OPTIONS']:
            Historique.objects.create(
                utilisateur=request.user.username,
                model_name=request.path,
                modifications={'method': request.method, 'path': request.path}
            )
        return response