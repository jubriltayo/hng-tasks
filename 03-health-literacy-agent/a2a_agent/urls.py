from django.urls import path
from .views.a2a_views import A2AHealthLiteracyView
from .views.health_views import HealthCheckView
from .views.basic_views import BasicHealthView
from .views.emergency import EmergencyView

urlpatterns = [
    path('a2a/health', A2AHealthLiteracyView.as_view(), name='a2a_health'),
    path('health', HealthCheckView.as_view(), name='health_check'),
    path('basic', BasicHealthView.as_view(), name='basic_health'),
    path('emergency', EmergencyView.as_view(), name='emergency'),
]