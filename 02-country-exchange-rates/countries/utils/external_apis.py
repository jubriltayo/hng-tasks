import requests
import logging
from typing import Dict, List
from django.utils import timezone

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
            params = {"fields": "name,capital,region,population,flags,currencies"}

            response = requests.get(cls.BASE_URL, params=params, timeout=30)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch country data: {str(e)}")
            raise ExternalAPIError("Could not fetch data from countries API")

    @classmethod
    def parse_country_data(cls, country_data: Dict) -> Dict:
        """Parse relevant fields from country data."""
        currencies = country_data.get("currencies", [])
        currency_code = currencies[0].get("code") if currencies else None

        population = country_data.get("population")
        if population is not None:
            try:
                population = int(population)
            except (TypeError, ValueError):
                population = 0

        return {
            "name": country_data.get("name"),
            "capital": country_data.get("capital"),
            "region": country_data.get("region"),
            "population": population,
            "currency_code": currency_code,
            "flag_url": country_data.get("flag"),
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

            if data.get("result") == "success":
                return data.get("rates", {})
            else:
                raise ExternalAPIError("Exchange rate API returned error")

        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch exchange rates: {str(e)}")
            raise ExternalAPIError("Could not fetch data from exchange rate API")


class DataRefreshService:
    @staticmethod
    def refresh_country_data():
        """Main service method to refresh country data."""
        from ..models import Country, SystemStatus

        try:
            # Fetch data from external APIs
            countries_data = CountryDataFetcher.fetch_all_countries()
            exchange_rates = ExchangeRateFetcher.fetch_exchange_rate()

            updated_countries = 0
            created_countries = 0
            skipped_countries = 0

            for country_data in countries_data:
                parsed_data = CountryDataFetcher.parse_country_data(country_data)

                if not parsed_data["name"] or parsed_data["population"] is None:
                    skipped_countries += 1
                    continue

                currency_code = parsed_data["currency_code"]
                exchange_rate = exchange_rates.get(currency_code) if currency_code else None

                if exchange_rate is not None:
                    from decimal import Decimal
                    exchange_rate = Decimal(str(exchange_rate))

                country_dict = {
                    "capital": parsed_data["capital"],
                    "region": parsed_data["region"],
                    "population": parsed_data["population"],
                    "currency_code": currency_code,
                    "exchange_rate": exchange_rate,
                    "flag_url": parsed_data["flag_url"],
                    "last_refreshed_at": timezone.now(),
                }

                try:
                    country, created = Country.objects.update_or_create(
                        name__iexact=parsed_data["name"], 
                        defaults=country_dict
                    )

                    if created:
                        created_countries += 1
                    else:
                        updated_countries += 1
                except Exception as e:
                    logger.error(f"Error processing country {parsed_data['name']}: {str(e)}")
                    skipped_countries += 1
                    continue

            # Update system status
            system_status = SystemStatus.get_current_status()
            system_status.update_status()

            return {
                "total_processed": len(countries_data),
                "created": created_countries,
                "updated": updated_countries,
                "skipped": skipped_countries,
            }

        except ExternalAPIError as e:
            logger.error(f"Data refresh failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during refresh: {str(e)}")
            raise ExternalAPIError(f"Refresh failed: {str(e)}")