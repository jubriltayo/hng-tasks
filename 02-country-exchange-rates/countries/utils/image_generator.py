from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings
from django.http import HttpResponse
from ..models import Country, SystemStatus

class SummaryImageGenerator:
    def __init__(self):
        self.image_path = os.path.join(settings.BASE_DIR, 'cache', 'summary.png')
        # Ensure cache directory exists
        os.makedirs(os.path.dirname(self.image_path), exist_ok=True)
    
    def generate_image(self):
        """Generate summary image with country data"""
        try:
            # Create image with white background
            image = Image.new('RGB', (800, 600), 'white')
            draw = ImageDraw.Draw(image)
            
            # Use default fonts to avoid encoding issues
            try:
                # Try to load fonts, but fallback to default if any issue
                title_font = ImageFont.truetype("arial.ttf", 32)
                header_font = ImageFont.truetype("arial.ttf", 24)
                body_font = ImageFont.truetype("arial.ttf", 18)
            except:
                # Use default font if there are any issues
                title_font = ImageFont.load_default()
                header_font = ImageFont.load_default()
                body_font = ImageFont.load_default()
            
            # Get data
            total_countries = Country.objects.count()
            top_countries = Country.objects.exclude(
                estimated_gdp__isnull=True
            ).order_by('-estimated_gdp')[:5]
            
            status = SystemStatus.get_current_status()
            
            # Draw content
            draw.text((50, 50), "Country GDP Summary", fill='black', font=title_font)
            draw.text((50, 100), f"Total Countries: {total_countries}", fill='black', font=header_font)
            draw.text((50, 130), f"Last Refresh: {status.last_refreshed_at}", fill='black', font=header_font)
            draw.text((50, 180), "Top 5 Countries by GDP:", fill='black', font=header_font)
            
            y = 220
            for i, country in enumerate(top_countries, 1):
                gdp = f"${country.estimated_gdp:,.2f}" if country.estimated_gdp else "N/A"
                text = f"{i}. {country.name}: {gdp}"
                draw.text((70, y), text, fill='black', font=body_font)
                y += 30
            
            # Save image as binary
            image.save(self.image_path, 'PNG')
            return True
            
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            return False
    
    def image_exists(self):
        """Check if summary image exists"""
        return os.path.exists(self.image_path)
    
    def get_image_response(self):
        """Return image as HTTP response"""
        try:
            with open(self.image_path, 'rb') as f:
                return HttpResponse(f.read(), content_type='image/png')
        except Exception as e:
            print(f"Error reading image: {str(e)}")
            return None
