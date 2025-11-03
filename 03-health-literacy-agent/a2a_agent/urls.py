from django.urls import path
from .views.a2a_views import A2AHealthLiteracyView
from .views.health_views import HealthCheckView

urlpatterns = [
    path('a2a/health', A2AHealthLiteracyView.as_view(), name='a2a_health'),
    path('health', HealthCheckView.as_view(), name='health_check'),
]