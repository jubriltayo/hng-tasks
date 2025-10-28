import requests
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class ExternalAPIError(Exception):
    """Custom exception for external API errors."""
    pass


class CountryDataFetcher:
    BASE_URL = "https://restcountries.com/v2/all"

    @classmethod
    def fetch_all_countries(cls) -> List[Dict]:
        """Fetch data for all countries from the countries API."""
        try:
            params = {
                'fields': 'name,capital,region,population,flags,currencies'
            }

            response = requests.get(cls.BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            
            return response.json()
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch country data: {str(e)}")
            raise ExternalAPIError("Could not fetch data from countries API")
        

    @classmethod
    def parse_country_data(cls, country_data: Dict) -> Dict:
        """Parse relevant fields from country data."""
        currencies = country_data.get('currencies', [])
        currency_code = currencies[0].get('code') if currencies else None
        
        return {
            'name': country_data.get('name'),
            'capital': country_data.get('capital'),
            'region': country_data.get('region'),
            'population': country_data.get('population'),
            'currency_code': currency_code,
            'flag_url': country_data.get('flags')
        }
    

class ExchangeRateFetcher:
    BASE_URL = "https://open.er-api.com/v6/latest/USD"

    @classmethod
    def fetch_exchange_rate(cls) -> Dict[str, float]:
        """Fetch exchange rates from ER API"""
        try:
            response = requests.get(cls.BASE_URL, timeout=30)
            response.raise_for_status()

            data = response.json()
            
            if data.get('result') == 'success':
                return data.get('rates', {})
            else:
                raise ExternalAPIError("Exchange rate API returned error")
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch exchange rates: {str(e)}")
            raise ExternalAPIError("Could not fetch data from exchange rate API")


class DataRefreshService:
    @staticmethod
    def refresh_country_data():
        """ Main service method to refresh country data. """
        from ..models import Country, SystemStatus

        try:
            # Fetch data from external APIs
            countries_data = CountryDataFetcher.fetch_all_countries()
            exchange_rates = ExchangeRateFetcher.fetch_exchange_rate()

            updated_countries = 0
            created_countries = 0

            for country_data in countries_data:
                parsed_data = CountryDataFetcher.parse_country_data(country_data)
                
                # Get exchange rate for the country's currency
                currency_code = parsed_data['currency_code']
                exchange_rate = None

                if currency_code:
                    exchange_rate = exchange_rates.get(currency_code)

                country_dict = {
                    'capital': parsed_data['capital'],
                    'region': parsed_data['region'],
                    'population': parsed_data['population'],
                    'currency_code': currency_code,
                    'exchange_rate': exchange_rate,
                    'flag_url': parsed_data['flag_url']
                }

                # Update or create country
                country, created = Country.objects.update_or_create(
                    name=parsed_data['name'],
                    defaults=country_dict
                )

                if created:
                    created_countries += 1
                else:
                    updated_countries += 1

            # Update system status
            system_status = SystemStatus.get_current_status()
            system_status.update_status()

            return {
                'total_processed': len(countries_data),
                'created': created_countries,
                'updated': updated_countries,
            }
        
        except ExternalAPIError as e:
            logger.error(f"Data refresh failed", {str(e)})
            raise
