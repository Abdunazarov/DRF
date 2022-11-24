from django.contrib import admin
from .models import BlogPost, BlogPostRus, BlogPostComments, Like, Dislike

admin.site.register(BlogPost)
admin.site.register(BlogPostRus)

admin.site.register(BlogPostComments)
admin.site.register(Like)
admin.site.register(Dislike)