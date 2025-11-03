import json
import logging
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from ..services.gemini_service import GeminiHealthService
from ..services.a2a_handler import A2ARequestHandler

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class A2AHealthLiteracyView(View):
    """Main A2A endpoint for Health Literacy Agent"""
    
    def __init__(self):
        super().__init__()
        self.health_service = GeminiHealthService()
        self.request_handler = A2ARequestHandler(self.health_service)
    
    def post(self, request):
        """Handle A2A protocol requests from Telex"""
        try:
            a2a_data = json.loads(request.body)
            response_data = self.request_handler.process_request(a2a_data)
            return JsonResponse(response_data)
            
        except json.JSONDecodeError:
            logger.error("Invalid JSON in request")
            return JsonResponse({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error: Invalid JSON"}
            })
        except Exception as e:
            logger.error(f"Unexpected error in A2A endpoint: {e}")
            return JsonResponse({
                "jsonrpc": "2.0", 
                "id": None,
                "error": {"code": -32603, "message": "Internal server error"}
            })