from django.urls import path
from .views import (
    StringAnalyzerView,
    StringDetailView,
    NaturalLanguageFilterView
)

urlpatterns = [
    path('strings/filter-by-natural-language', NaturalLanguageFilterView.as_view(), name='natural-language-filter'),

    path('strings', StringAnalyzerView.as_view(), name='string-list-create'),
    path('strings/<path:string_value>', StringDetailView.as_view(), name='string-detail')
]
