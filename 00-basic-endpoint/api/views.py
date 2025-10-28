import requests
from datetime import datetime, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class MeView(APIView):
    def get(self, request):
        try:
            response = requests.get("https://catfact.ninja/fact", timeout=5)
            response.raise_for_status()
            fact = response.json().get("fact", "No fact found.")
        except Exception:
            fact = "Cat fact service is currently unavailable."

        data = {
            "status": "success",
            "user": {
                "email": "jubriltayo@gmail.com",
                "name": "Tayo Jubril",
                "stack": "Python (Django, FastAPI, Flask), JavaScript (Node.js, React, Next.js), PHP (Laravel)",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "fact": fact,
        }

        return Response(data, status=status.HTTP_200_OK)
