from django.db import models
from django.utils import timezone
import hashlib
import json


class AnalyzedString(models.Model):
    id = models.CharField(primary_key=True, max_length=64, editable=False)
    value = models.TextField(unique=True)
    length = models.IntegerField()
    is_palindrome = models.BooleanField()
    unique_characters = models.IntegerField()
    word_count = models.IntegerField()
    sha256_hash = models.CharField(max_length=64, unique=True)
    character_frequency_map = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'analyzed_strings'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_palindrome']),
            models.Index(fields=['word_count']),
            models.Index(fields=['length']),
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            self.compute_properties()
        super().save(*args, **kwargs)

    def compute_properties(self):
        # SHA-256 hash
        self.sha256_hash = hashlib.sha256(self.value.encode('utf-8')).hexdigest()
        self.id = self.sha256_hash

        # Length
        self.length = len(self.value)

        # Palindrome check (case-insensitive)
        cleaned_value = self.value.lower()
        self.is_palindrome = cleaned_value == cleaned_value[::-1]

        # Unique characters
        self.unique_characters = len(set(self.value))

        # Word count
        self.word_count = len(self.value.split())

        # Character frequency map
        char_freq = {}
        for char in self.value:
            char_freq[char] = char_freq.get(char, 0) + 1
        self.character_frequency_map = char_freq

    def __str__(self):
        return f"{self.value[:50]}... ({self.sha256_hash[:8]})"
