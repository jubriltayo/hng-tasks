from django.http import JsonResponse
from django.views import View
from datetime import datetime

from ..services.gemini_service import GeminiHealthService

class HealthCheckView(View):
    """Health check endpoint for monitoring"""
    
    def get(self, request):
        health_service = GeminiHealthService()
        return JsonResponse({
            "status": "healthy",
            "service": "HealthLiteracy AI Agent",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "gemini_available": health_service.available,
            "version": "1.0.0"
        })