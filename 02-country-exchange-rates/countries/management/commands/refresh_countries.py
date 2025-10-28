from django.core.management.base import BaseCommand
from countries.utils.external_apis import DataRefreshService
from countries.utils.image_generator import SummaryImageGenerator

class Command(BaseCommand):
    help = 'Refresh country data from external APIs'
    
    def handle(self, *args, **options):
        try:
            self.stdout.write('Starting country data refresh...')
            
            result = DataRefreshService.refresh_country_data()
            
            # Generate summary image
            image_generator = SummaryImageGenerator()
            image_generator.generate_image()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully refreshed {result['total_processed']} countries. "
                    f"Created: {result['created']}, Updated: {result['updated']}"
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error refreshing country data: {str(e)}")
            )