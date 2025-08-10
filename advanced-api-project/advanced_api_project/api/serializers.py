from rest_framework import serializers
from datetime import datetime
from .models import Author, Book
                          
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model= Book
        fields= '__all__'
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value
class AutherSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ['name', 'books']
        