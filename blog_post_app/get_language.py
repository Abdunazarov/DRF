from .models import BlogPost, BlogPostRus
from django.shortcuts import get_object_or_404
from rest_framework import serializers

def get_language(lan, pk):

    if lan == 'ru':
        try:
            post = BlogPostRus.objects.get(id=pk)
        except BlogPostRus.DoesNotExist:
            raise serializers.ValidationError({'Error': 'There is no such blog post'})
    elif lan == 'en':
        try:
            post = BlogPost.objects.get(id=pk)
        except BlogPost.DoesNotExist:
            raise serializers
    return post