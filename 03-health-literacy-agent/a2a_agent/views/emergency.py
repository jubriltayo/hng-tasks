from django.http import JsonResponse
from django.views import View

class EmergencyView(View):
    def get(self, request):
        return JsonResponse({"status": "EMERGENCY WORKS"})