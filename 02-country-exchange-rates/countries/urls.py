from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountryViewSet, StatusViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'status', StatusViewSet, basename='status')

urlpatterns = [
    path('', include(router.urls)),

    path('countries/image', CountryViewSet.as_view({'get': 'image'}), name='countries-image'),
]