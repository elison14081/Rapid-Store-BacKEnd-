from django.conf import settings
from django.http import JsonResponse

class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lista de rutas públicas (con y sin barra final)
        public_paths = [
            '/admin', '/admin/', '/static', '/static/', '/media', '/media/',
            '/api/users/register', '/api/users/register/',
            '/api/users/login', '/api/users/login/',
            '/api/token', '/api/token/',
            '/api/token/refresh', '/api/token/refresh/'
        ]
        if any(request.path.startswith(path) for path in public_paths):
            return self.get_response(request)

        api_key = request.headers.get('X-API-KEY')
        if api_key != settings.API_KEY:
            return JsonResponse({'detail': 'Invalid or missing API Key.'}, status=401)
        return self.get_response(request)