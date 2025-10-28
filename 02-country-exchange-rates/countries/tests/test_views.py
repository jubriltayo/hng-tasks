from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from countries.models import Country, SystemStatus
from decimal import Decimal

class CountryViewSetTest(APITestCase):
    def setUp(self):
        # Clear existing data
        Country.objects.all().delete()
        
        # Create test data with VERY CLEAR GDP ordering
        self.country1 = Country.objects.create(
            name='Nigeria',
            capital='Abuja',
            region='Africa',
            population=100000000,
            currency_code='NGN',
            exchange_rate=Decimal('1500.0'),
            estimated_gdp=Decimal('1000000.00')  # 1M GDP - LOWEST
        )
        self.country2 = Country.objects.create(
            name='Ghana',
            capital='Accra',
            region='Africa', 
            currency_code='GHS',
            population=50000000,
            exchange_rate=Decimal('10.0'),
            estimated_gdp=Decimal('5000000.00')  # 5M GDP - MIDDLE
        )
        self.country3 = Country.objects.create(
            name='United States',
            capital='Washington DC',
            region='Americas',
            population=300000000,
            currency_code='USD',
            exchange_rate=Decimal('1.0'),
            estimated_gdp=Decimal('9000000.00')  # 9M GDP - HIGHEST
        )
        
    def test_get_country_by_name(self):
        """Test retrieving country by name (case insensitive)"""
        # Test exact match
        url = reverse('country-detail', kwargs={'name': 'Nigeria'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Nigeria')
        
        # Test case insensitive match
        url = reverse('country-detail', kwargs={'name': 'nigerIA'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Nigeria')
    
    def test_get_nonexistent_country(self):
        """Test 404 for non-existent country"""
        url = reverse('country-detail', kwargs={'name': 'Nonexistent'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Country not found')
    
    def test_delete_country(self):
        """Test deleting country by name"""
        url = reverse('country-detail', kwargs={'name': 'Ghana'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify country was deleted
        self.assertFalse(Country.objects.filter(name='Ghana').exists())
    
    def test_delete_nonexistent_country(self):
        """Test 404 when deleting non-existent country"""
        url = reverse('country-detail', kwargs={'name': 'Nonexistent'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_filter_by_region(self):
        """Test filtering countries by region"""
        url = reverse('country-list') + '?region=Africa'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Nigeria and Ghana
    
    def test_filter_by_currency(self):
        """Test filtering countries by currency"""
        url = reverse('country-list') + '?currency=USD'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['currency_code'], 'USD')
    
    def test_sort_by_gdp_desc(self):
        """Test sorting countries by GDP descending"""
        url = reverse('country-list') + '?sort=gdp_desc'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        countries = response.data
        self.assertEqual(countries[0]['name'], 'United States')
        self.assertEqual(countries[1]['name'], 'Ghana')
        self.assertEqual(countries[2]['name'], 'Nigeria')

    def test_sort_by_gdp_asc(self):
        """Test sorting countries by GDP ascending"""
        url = reverse('country-list') + '?sort=gdp_asc'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        countries = response.data
        self.assertEqual(countries[0]['name'], 'Nigeria')
        self.assertEqual(countries[1]['name'], 'Ghana') 
        self.assertEqual(countries[2]['name'], 'United States')

class StatusViewTest(APITestCase):
    def test_status_endpoint(self):
        """Test system status endpoint"""
        # Create some test countries
        Country.objects.create(name='Test1', population=1000000)
        Country.objects.create(name='Test2', population=2000000)
        
        url = reverse('status-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_countries'], 2)
        self.assertIn('last_refreshed_at', response.data)  # Critical test!