from django.http import JsonResponse
from django.views import View

class BasicHealthView(View):
    def get(self, request):
        return JsonResponse({"status": "basic health works"})