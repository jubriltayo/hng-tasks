from django.test import TestCase
from django.core.exceptions import ValidationError
from countries.models import Country, SystemStatus
from decimal import Decimal
import random

class CountryModelTest(TestCase):
    def setUp(self):
        self.country_data = {
            'name': 'Test Country',
            'capital': 'Test Capital',
            'region': 'Test Region',
            'population': 1000000,
            'currency_code': 'USD',
            'exchange_rate': Decimal('1.0'),
            'flag_url': 'https://example.com/flag.png'
        }
    
    def test_country_creation(self):
        """Test that country can be created with required fields"""
        country = Country.objects.create(**self.country_data)
        self.assertEqual(country.name, 'Test Country')
        self.assertEqual(country.population, 1000000)
        self.assertIsNotNone(country.estimated_gdp)
    
    def test_gdp_calculation(self):
        """Test GDP calculation formula"""
        country = Country.objects.create(**self.country_data)
        calculated_gdp = country.calculate_estimated_gdp()
        
        # GDP should be between population*1000/exchange_rate and population*2000/exchange_rate
        min_expected = (1000000 * 1000) / 1.0
        max_expected = (1000000 * 2000) / 1.0
        
        self.assertGreaterEqual(calculated_gdp, min_expected)
        self.assertLessEqual(calculated_gdp, max_expected)
    
    def test_gdp_with_string_population(self):
        """Test GDP calculation with string population (edge case)"""
        country_data = self.country_data.copy()
        country_data['population'] = '1000000'  # String population
        country = Country(**country_data)
        
        # This should not raise TypeError
        gdp = country.calculate_estimated_gdp()
        self.assertIsNotNone(gdp)
    
    def test_required_fields(self):
        """Test that name and population are required"""
        with self.assertRaises(ValidationError):
            country = Country(name=None, population=1000000)
            country.full_clean()
        
        with self.assertRaises(ValidationError):
            country = Country(name='Test', population=None)
            country.full_clean()

class SystemStatusTest(TestCase):
    def test_system_status_creation(self):
        """Test system status singleton pattern"""
        status1 = SystemStatus.get_current_status()
        status2 = SystemStatus.get_current_status()
        
        self.assertEqual(status1.pk, status2.pk)
        self.assertEqual(status1.total_countries, 0)
    
    def test_system_status_fields(self):
        """Test that system status has correct fields"""
        status = SystemStatus.get_current_status()
        
        # Check that last_refreshed_at field exists (not last_updated)
        self.assertTrue(hasattr(status, 'last_refreshed_at'))
        self.assertFalse(hasattr(status, 'last_updated'))  # Should not exist