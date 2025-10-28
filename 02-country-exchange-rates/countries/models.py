from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
import random


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    capital = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=50, null=True, blank=True)
    population = models.BigIntegerField(validators=[MinValueValidator(0)])
    currency_code = models.CharField(max_length=10, null=True, blank=True)
    exchange_rate = models.DecimalField(
        max_digits=20,
        decimal_places=6,
        null=True,
        blank=True,
    )
    estimated_gdp = models.DecimalField(
        max_digits=30,
        decimal_places=2,
        null=True,
        blank=True,
    )
    flag_url = models.URLField(max_length=500, null=True, blank=True)
    last_refreshed_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'countries'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['region']),
            models.Index(fields=['currency_code']),
            models.Index(fields=['estimated_gdp']),
        ]

    def calculate_estimated_gdp(self):
        """ Calculate estimated GDP based on population and exchange rate. """
        if self.population and self.exchange_rate:
            random_multiplier = random.uniform(1000, 2000)
            gdp = (self.population * random_multiplier) / float(self.exchange_rate)
            return round(gdp, 2)
        return None
    
    def save(self, *args, **kwargs):
        # Calculate estimated GDP before saving
        if self.population and self.exchange_rate:
            self.estimated_gdp = self.calculate_estimated_gdp()
        else:
            self.estimated_gdp = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class SystemStatus(models.Model):
    total_countries = models.IntegerField(default=0)
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'system_status'

    @classmethod
    def get_current_status(cls):
        status, created = cls.objects.get_or_create(pk=1) # Singleton pattern - enforce only one row
        if created:
            status.total_countries = Country.objects.count()
            status.save()
        return status
    
    def update_status(self):
        self.total_countries = Country.objects.count()
        self.last_updated = timezone.now()
        self.save()
