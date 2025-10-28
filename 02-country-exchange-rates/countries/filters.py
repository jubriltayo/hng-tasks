import django_filters
from .models import Country


class CountryFilter(django_filters.FilterSet):
    region = django_filters.CharFilter(field_name="region", lookup_expr="iexact")
    currency = django_filters.CharFilter(
        field_name="currency_code", lookup_expr="iexact"
    )

    # Custom sorting for GDP
    sort = django_filters.CharFilter(method="filter_sort")

    class Meta:
        model = Country
        fields = ["region", "currency_code"]

    def filter_sort(self, queryset, name, value):
        """Handle custom sorting"""
        if value == 'gdp_desc':
            return queryset.order_by('-estimated_gdp', 'name')
        elif value == 'gdp_asc':
            non_null = queryset.filter(estimated_gdp__isnull=False).order_by('estimated_gdp', 'name')
            nulls = queryset.filter(estimated_gdp__isnull=True).order_by('name')
            return non_null.union(nulls)
        elif value == "population_desc":
            return queryset.order_by("-population")
        elif value == "population_asc":
            return queryset.order_by("population")
        elif value == "name_asc":
            return queryset.order_by("name")
        elif value == "name_desc":
            return queryset.order_by("-name")

        # Default sorting
        return queryset.order_by("name")
