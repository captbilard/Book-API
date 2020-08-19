from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin

from .models import Publisher, Book, Author

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ('__all__')

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('__all__')

class BookSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('__all__')
        depth = 1