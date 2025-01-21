from django.utils import timezone
from .models import Historique

class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated and request.method not in ['GET', 'HEAD', 'OPTIONS']:
            instance_id = self.get_instance_id_from_request(request)
            if instance_id:
                Historique.objects.create(
                    utilisateur=request.user.username,
                    model_name=request.path,
                    instance_id=instance_id,
                    modifications={'method': request.method, 'path': request.path}
                )
        return response

    def get_instance_id_from_request(self, request):
        # Logic to extract instance_id from the request
        # For example, you might extract it from the URL or request data
        print(request.POST)

        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            if 'id_employe' in request.POST:
                return request.POST.get('id_employe')
            else:
                # Assuming the instance ID is the last part of the URL
                try:
                    return int(request.path.split('/')[-2])
                except (ValueError, IndexError):
                    return None
        return None