from django.test import TestCase
from countries.models import Country
from countries.filters import CountryFilter
from decimal import Decimal

class CountryFilterTest(TestCase):
    def setUp(self):
        # Create test countries with different GDP values (including NULL)
        self.country1 = Country.objects.create(
            name='High GDP Country',
            population=100000000,
            exchange_rate=Decimal('1.0'),
            estimated_gdp=Decimal('150000000000.0')  # High GDP
        )
        self.country2 = Country.objects.create(
            name='Low GDP Country', 
            population=5000000,
            exchange_rate=Decimal('1.0'),
            estimated_gdp=Decimal('7500000000.0')  # Low GDP
        )
        self.country3 = Country.objects.create(
            name='No GDP Country',
            population=1000000,
            exchange_rate=None,  # No exchange rate = no GDP
            estimated_gdp=None
        )
    
    def test_gdp_asc_sorting(self):
        """Test GDP ascending sorting with NULL values"""
        queryset = Country.objects.all()
        filter = CountryFilter()
        
        # Sort by GDP ascending - NULL values should be last
        sorted_qs = filter.filter_sort(queryset, 'sort', 'gdp_asc')
        sorted_countries = list(sorted_qs)
        
        # With our simple approach, NULLs come last
        self.assertEqual(sorted_countries[0].name, 'Low GDP Country')
        self.assertEqual(sorted_countries[1].name, 'High GDP Country')
        self.assertEqual(sorted_countries[2].name, 'No GDP Country')  # NULLs last

    def test_gdp_desc_sorting(self):
        """Test GDP descending sorting with NULL values"""
        queryset = Country.objects.all()
        filter = CountryFilter()
        
        # Sort by GDP descending - NULL values should be last
        sorted_qs = filter.filter_sort(queryset, 'sort', 'gdp_desc')
        sorted_countries = list(sorted_qs)
        
        # With our simple approach, NULLs come last in descending too
        self.assertEqual(sorted_countries[0].name, 'High GDP Country')
        self.assertEqual(sorted_countries[1].name, 'Low GDP Country') 
        self.assertEqual(sorted_countries[2].name, 'No GDP Country')  # NULLs last