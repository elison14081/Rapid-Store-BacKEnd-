from django.conf import settings
from django.http import JsonResponse

class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Excluye admin y static/media
        if request.path.startswith('/admin/') or request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)
        # Puedes excluir otras rutas si lo deseas

        api_key = request.headers.get('X-API-KEY')
        if api_key != settings.API_KEY:
            return JsonResponse({'detail': 'Invalid or missing API Key.'}, status=401)
        return self.get_response(request)