from django.contrib import admin
from .models import BlogPost, BlogPostRus, BlogNotAllowedTo, BlogPostComments

admin.site.register(BlogPost)
admin.site.register(BlogPostRus)
admin.site.register(BlogNotAllowedTo)

admin.site.register(BlogPostComments)