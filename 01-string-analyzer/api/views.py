from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.db.models import Q
import re

from .models import AnalyzedString
from .serializers import (
    AnalyzedStringSerializer,
    StringCreateSerializer,
    StringListSerializer,
    NaturalLanguageFilterSerializer
)


class StringAnalyzerView(APIView):
    """
    POST /strings - Create and analyze a new string
    GET /strings - List all strings with optional filters
    """

    def post(self, request):
        serializer = StringCreateSerializer(data=request.data)

        if not serializer.is_valid():
            if 'value' not in request.data:
                return Response(
                    {'error':'Missing "value" field in request body'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            analyzed_string = serializer.save()
            response_serializer = AnalyzedStringSerializer(analyzed_string)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                {'error': 'String already exists in the system'},
                status=status.HTTP_409_CONFLICT
            )


    def get(self, request):
        queryset = AnalyzedString.objects.all()
        filters_applied = {}

        # Apply filters
        try:
            # is_palindrome filter
            is_palindrome = request.query_params.get('is_palindrome')
            if is_palindrome is not None:
                is_palindrome_bool = self._parse_boolean(is_palindrome)
                if is_palindrome_bool is None:
                    return Response(
                        {'error': 'Invalid value for is_palindrome. Must be true or false.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                queryset = queryset.filter(is_palindrome=is_palindrome_bool)
                filters_applied['is_palindrome'] = is_palindrome_bool

            # min_length filter
            min_length = request.query_params.get('min_length')
            if min_length is not None:
                try:
                    min_length_int = int(min_length)
                    queryset = queryset.filter(length__gte=min_length_int)
                    filters_applied['min_length'] = min_length_int
                except ValueError:
                    return Response(
                        {'error': 'Invalid value for min_length. Must be an integer.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # max_length filter
            max_length = request.query_params.get('max_length')
            if max_length is not None:
                try:
                    max_length_int = int(max_length)
                    queryset = queryset.filter(length__lte=max_length_int)
                    filters_applied['max_length'] = max_length_int
                except ValueError:
                    return Response(
                        {'error': 'Invalid value for max_length. Must be an integer.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # word_count filter
            word_count = request.query_params.get('word_count')
            if word_count is not None:
                try:
                    word_count_int = int(word_count)
                    queryset = queryset.filter(word_count=word_count_int)
                    filters_applied['word_count'] = word_count_int
                except ValueError:
                    return Response(
                        {'error': 'Invalid value for word_count. Must be an integer.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # contains_character filter
            contains_character = request.query_params.get('contains_character')
            if contains_character is not None:
                if len(contains_character) != 1:
                    return Response(
                        {'error': 'contains_character must be a single character.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                queryset = queryset.filter(value__contains=contains_character)
                filters_applied['contains_character'] = contains_character
        
        except Exception as e:
            return Response(
                {'error': f'Invalid query parameters: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Serialize response
        serializer = AnalyzedStringSerializer(queryset, many=True)
        response_data = {
            'data': serializer.data,
            'count': queryset.count(),
            'filters_applied': filters_applied
        } 

        return Response(response_data, status=status.HTTP_200_OK)   

    def _parse_boolean(self, value):
        """Parse a string to boolean."""
        true_set = ['true', '1', 'yes']
        false_set = ['false', '0', 'no']
        value_lower = value.lower()
        if value_lower in true_set:
            return True
        elif value_lower in false_set:
            return False
        return None
    

class StringDetailView(APIView):
    """
    GET /strings/{string_value} - Get a specific string
    DELETE /strings/{string_value} - Delete a specific string
    """

    def get(self, request, string_value):
        try:
            analyzed_string = AnalyzedString.objects.get(value=string_value)
            serializer = AnalyzedStringSerializer(analyzed_string)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AnalyzedString.DoesNotExist:
            return Response(
                {'error': 'String does not exist in the system'},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, string_value):
        try:
            analyzed_string = AnalyzedString.objects.get(value=string_value)
            analyzed_string.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AnalyzedString.DoesNotExist:
            return Response(
                {'error': 'String does not exist in the system'},
                status=status.HTTP_404_NOT_FOUND
            )
        

class NaturalLanguageFilterView(APIView):
    """
    GET /strings/filter-by-natural-language - Filter strings using natural language
    """

    def get(self, request):
        query = request.query_params.get('query')
        
        if not query:
            return Response(
                {'error': 'Query parameter is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Parse natural language query
            parsed_filters = self._parse_natural_language(query)

            if not parsed_filters:
                return Response(
                    {'error': 'Unable to parse the natural language query'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check for conflicting filters
            if 'min_length' in parsed_filters and 'max_length' in parsed_filters:
                if parsed_filters['min_length'] > parsed_filters['max_length']:
                    return Response(
                        {'error': 'Query parsed but resulted in conflicting filters'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY
                    )
            
            # Apply filters to queryset
            queryset = AnalyzedString.objects.all()
            
            if 'is_palindrome' in parsed_filters:
                queryset = queryset.filter(is_palindrome=parsed_filters['is_palindrome'])
            
            if 'word_count' in parsed_filters:
                queryset = queryset.filter(word_count=parsed_filters['word_count'])
            
            if 'min_length' in parsed_filters:
                queryset = queryset.filter(length__gte=parsed_filters['min_length'])
            
            if 'max_length' in parsed_filters:
                queryset = queryset.filter(length__lte=parsed_filters['max_length'])
            
            if 'contains_character' in parsed_filters:
                queryset = queryset.filter(value__contains=parsed_filters['contains_character'])
            
            # Serialize response
            serializer = AnalyzedStringSerializer(queryset, many=True)
            response_data = {
                'data': serializer.data,
                'count': queryset.count(),
                'interpreted_query': {
                    'original': query,
                    'parsed_filters': parsed_filters
                }
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error processing query: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def _parse_natural_language(self, query):
        """Parse natural language query into filters."""
        query_lower = query.lower()
        filters = {}

        # Palindrome detection
        if any(word in query_lower for word in ['palindrome', 'palindromic', 'reads same']):
            filters['is_palindrome'] = True
        
        # Word count detection
        if 'single word' in query_lower or 'one word' in query_lower:
            filters['word_count'] = 1
        elif 'two word' in query_lower or 'two words' in query_lower:
            filters['word_count'] = 2
        elif 'three word' in query_lower or 'three words' in query_lower:
            filters['word_count'] = 3
        elif 'four word' in query_lower or 'four words' in query_lower:
            filters['word_count'] = 4
        elif 'five word' in query_lower or 'five words' in query_lower:
            filters['word_count'] = 5
        else:
            # Extract number + word(s)
            word_count_match = re.search(r'(\d+)\s+words?', query_lower)
            if word_count_match:
                filters['word_count'] = int(word_count_match.group(1))
        
        # Length detection
        longer_match = re.search(r'longer than (\d+)', query_lower)
        if longer_match:
            filters['min_length'] = int(longer_match.group(1)) + 1
        
        shorter_match = re.search(r'shorter than (\d+)', query_lower)
        if shorter_match:
            filters['max_length'] = int(shorter_match.group(1)) - 1
        
        # Character detection
        if 'containing the letter' in query_lower or 'contains the letter' in query_lower:
            letter_match = re.search(r'letter ([a-z])', query_lower)
            if letter_match:
                filters['contains_character'] = letter_match.group(1)
        
        return filters
