from rest_framework import serializers
from .models import BlogPost, BlogPostComments


class BlogPostSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(read_only=True, format="%Y-%m-%d (%X)")
    date_updated = serializers.DateTimeField(read_only=True, format="%Y-%m-%d (%X)")
    text = serializers.CharField(required=False)
    author = serializers.CharField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'image', 'date_created', 'date_updated')
        model = BlogPost



class BlogPostCommentsSerializer(serializers.Serializer):
    date_created = serializers.DateTimeField(read_only=True, format="%Y-%m-%d (%X)")
    body = serializers.CharField()


    def save(self, validated_data, blog_post, user):
        new_comment = BlogPostComments.objects.create(
            user=user,
            post=blog_post,
            body=validated_data['body']
        )
        return new_comment
