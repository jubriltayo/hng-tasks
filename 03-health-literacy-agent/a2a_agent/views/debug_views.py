import os
from django.http import JsonResponse
from django.views import View

class EnvironmentCheckView(View):
    """Temporary view to check environment variables"""
    
    def get(self, request):
        return JsonResponse({
            'GEMINI_API_KEY_set': bool(os.getenv('GEMINI_API_KEY')),
            'GEMINI_API_KEY_value': '***' if os.getenv('GEMINI_API_KEY') else 'NOT SET',
            'SECRET_KEY_set': bool(os.getenv('SECRET_KEY')),
            'DEBUG': os.getenv('DEBUG', 'Not set'),
            'railway_environment': 'PRODUCTION' if os.getenv('RAILWAY_ENVIRONMENT') else 'UNKNOWN'
        })