from rest_framework import serializers
from .models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(read_only=True, format="%Y-%m-%d (%X)")
    date_updated = serializers.DateTimeField(read_only=True, format="%Y-%m-%d (%X)")
    author = serializers.CharField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'image', 'date_created', 'date_updated')
        model = BlogPost

