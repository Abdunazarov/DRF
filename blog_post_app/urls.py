from django.urls import path
from .views import *


urlpatterns = [
    # path('all/', blog_post_list),
    path('all/', BlogPostListView.as_view()),

    path('create/', create_blog_post), 
    path('delete/<pk>/', delete_blog_post),
    path('detail/<pk>/', detail_blog_post),
    path('update/<pk>/', update_blog_post),

    path('create_front/', create_blog_front)

]