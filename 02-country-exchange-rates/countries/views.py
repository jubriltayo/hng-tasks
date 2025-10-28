from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
import logging

from .models import Country, SystemStatus
from .serializers import CountrySerializer, SystemStatusSerializer
from .utils.external_apis import DataRefreshService, ExternalAPIError
from .utils.image_generator import SummaryImageGenerator
from .filters import CountryFilter

logger = logging.getLogger(__name__)


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CountryFilter
    # ordering_fields = ['name', 'population', 'estimated_gdp']
    # ordering = ['name']
    lookup_field = 'name'
    lookup_url_kwarg = 'name'

    def get_serializer_class(self):
        return CountrySerializer
    
    def list(self, request, *args, **kwargs):
        """Get all countries with filtering and sorting"""
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error listing countries: {str(e)}")
            return Response(
                {"error": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, *args, **kwargs):
        """Get one country by name"""
        try:
            name = kwargs.get('name')
            instance = Country.objects.get(name__iexact=name)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Country.DoesNotExist:
            return Response(
                {"error": "Country not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error retrieving country: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    def destroy (self, request, *args, **kwargs):
        """Delete a country record"""
        try:
            name = kwargs.get('name')
            instance = Country.objects.get(name__iexact=name)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Country.DoesNotExist:
            return Response(
                {"error": "Country not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error deleting country: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(detail=False, methods=['post'])
    def refresh(self, request):
        """ Fetch all countries and exchange rates, then cache them in the database """
        try:
            result = DataRefreshService.refresh_country_data()
            
            # Generate summary image after refresh
            image_generator = SummaryImageGenerator()
            image_generator.generate_image()
            
            return Response({
                "message": "Country data refreshed successfully.",
                "data": result
            })
        except ExternalAPIError as e:
            return Response({
                "error": "External data source unavailable",
                "details": str(e)   
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
        except Exception as e:
            logger.error(f"Error refreshing country data: {str(e)}")
            return Response(
                {"error": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(detail=False, methods=['get'])
    def image(self, request):
        """Serve the generated summary image"""
        image_generator = SummaryImageGenerator()
        
        # If image doesn't exist, try to generate it first
        if not image_generator.image_exists():
            # Try to generate the image
            if not image_generator.generate_image():
                return Response(
                    {"error": "Summary image not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Get image response
        response = image_generator.get_image_response()
        if response:
            return response
        else:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    
class StatusViewSet(viewsets.ViewSet):
    def list(self, request):
        """ Show total countries and last updated timestamp """
        try:
            status_obj = SystemStatus.get_current_status()
            serializer = SystemStatusSerializer(status_obj)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving system status: {str(e)}")
            return Response(
                {"error": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
