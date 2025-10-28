from rest_framework import serializers
from .models import AnalyzedString


class AnalyzedStringSerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField() # Read-only nested properties field

    class Meta:
        model = AnalyzedString
        fields = ['id', 'value', 'properties', 'created_at']
        read_only_fields = ['id', 'properties', 'created_at']

    def get_properties(self, obj):
        """Return the computed properties as a nested dictionary."""

        return {
            'length': obj.length,
            'is_palindrome': obj.is_palindrome,
            'unique_characters': obj.unique_characters,
            'word_count': obj.word_count,
            'sha256_hash': obj.sha256_hash,
            'character_frequency_map': obj.character_frequency_map,
        }
    

class StringCreateSerializer(serializers.Serializer):
    value = serializers.CharField(required=True, allow_blank=False)

    def validate_value(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Value must not be a string")
        return value
    
    def create(self, validated_data):
        return AnalyzedString.objects.create(**validated_data)
    

class StringListSerializer(serializers.Serializer):
    """ Serializer for list response with param filters """
    
    data = AnalyzedStringSerializer(many=True)
    count = serializers.IntegerField()
    filters_applied = serializers.DictField()


class NaturalLanguageFilterSerializer(serializers.Serializer):
    """ Serializer for natural language filter response """
    
    data = AnalyzedStringSerializer(many=True)
    count = serializers.IntegerField()
    interpreted_query = serializers.DictField()
