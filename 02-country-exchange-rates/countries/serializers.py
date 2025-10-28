from rest_framework import serializers
from .models import Country, SystemStatus


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = [
            'id',
            'name',
            'capital',
            'region',
            'population',
            'currency_code',
            'exchange_rate',
            'estimated_gdp',
            'flag_url',
            'last_refreshed_at',
        ]
    

class SystemStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemStatus
        fields = [
            'total_countries',
            'last_refreshed_at',
        ]
