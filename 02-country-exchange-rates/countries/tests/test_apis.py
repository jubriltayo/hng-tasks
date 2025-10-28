from django.test import TestCase
from unittest.mock import patch, MagicMock
from countries.utils.external_apis import CountryDataFetcher, ExchangeRateFetcher, DataRefreshService, ExternalAPIError
from countries.models import Country
import json

class ExternalAPIsTest(TestCase):
    @patch('countries.utils.external_apis.requests.get')
    def test_country_data_fetcher_success(self, mock_get):
        """Test successful country data fetching"""
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                'name': 'Test Country',
                'capital': 'Test Capital',
                'region': 'Test Region',
                'population': 1000000,
                'flag': 'https://example.com/flag.png',
                'currencies': [{'code': 'USD'}]
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        countries = CountryDataFetcher.fetch_all_countries()
        
        self.assertEqual(len(countries), 1)
        self.assertEqual(countries[0]['name'], 'Test Country')
        self.assertEqual(countries[0]['population'], 1000000)  # Should be int
    
    @patch('countries.utils.external_apis.requests.get')
    def test_exchange_rate_fetcher_success(self, mock_get):
        """Test successful exchange rate fetching"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'result': 'success',
            'rates': {'USD': 1.0, 'NGN': 1600.0, 'EUR': 0.85}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        rates = ExchangeRateFetcher.fetch_exchange_rate()
        
        self.assertEqual(rates['USD'], 1.0)
        self.assertEqual(rates['NGN'], 1600.0)
        self.assertEqual(len(rates), 3)
    
    def test_parse_country_data_types(self):
        """Test that parsed country data has correct types"""
        sample_data = {
            'name': 'Test Country',
            'capital': 'Test Capital',
            'region': 'Test Region',
            'population': '1000000',  # String population
            'flag': 'https://example.com/flag.png',
            'currencies': [{'code': 'USD'}]
        }
        
        parsed = CountryDataFetcher.parse_country_data(sample_data)
        
        # Population should be converted to int
        self.assertIsInstance(parsed['population'], int)
        self.assertEqual(parsed['population'], 1000000)
        
        # Other fields should maintain correct types
        self.assertIsInstance(parsed['name'], str)
        self.assertIsInstance(parsed['currency_code'], str)