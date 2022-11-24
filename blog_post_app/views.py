from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from django.shortcuts import get_object_or_404

from .models import *
from .serializers import *

from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import ListAPIView
from rest_framework import filters

# translation 

class BlogPostListView(ListAPIView):
    search_fields = ['text', 'author__email'] # ForeignKey or ManyToMany field should be filtered this way!
    filter_backends = (filters.SearchFilter,)
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

from .models import User


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_blog_post(request):

    author = request.user 
    blog_post = BlogPost(author=author)
    serializer = BlogPostSerializer(blog_post, data=request.data)

    if serializer.is_valid():
        serializer.save()
        print(serializer.data)
        return Response(serializer.data)

    return Response(serializer.errors)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def detail_blog_post(request, pk):

    # post = ru_or_en(lan=request.LANGUAGE_CODE, pk=pk, first_lang_obj=BlogPost, second_lan_obj=BlogPostRus)
    post = get_object_or_404(BlogPost, id=pk)
    print(post)
    comments = []
    all_comments = BlogPostComments.objects.filter(post=post)
    for comment in all_comments:
        comments.append(comment.id)

    likes = Like.objects.filter(blog_post=post).count()
    dislikes = Dislike.objects.filter(blog_post=post).count()


    data = BlogPostSerializer(post).data
    data['comments'] = comments
    data['likes'] = likes
    data['dislikes'] = dislikes

    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like(request, pk):
    post = get_object_or_404(BlogPost, id=pk)
    user = request.user

 
    if not Like.objects.filter(who_liked=user, blog_post=post).exists():  # !!!!!
        Like.objects.create(who_liked=user, blog_post=post)
        return Response({'Response': 'Post liked!'})
    

    Like.objects.get(who_liked=user, blog_post=post).delete()

    return Response({'Response': 'Like removed from post!'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dislike(request, pk):
    post = get_object_or_404(BlogPost, id=pk)
    user = request.user
 
    if not Dislike.objects.filter(who_disliked=user, blog_post=post).exists():  # !!!!!
        Dislike.objects.create(who_disliked=user, blog_post=post)
        return Response({'Response': 'Post disliked!'})


    Dislike.objects.get(who_disliked=user, blog_post=post).delete()
    return Response({'Response': 'Dislike removed from post!'})







@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_one(request, pk):
    post = BlogPost.objects.get(id=pk)
    user = request.user

    try:
        not_allowed = BlogNotAllowedTo.objects.get(user=user, post=post)
    
    except BlogNotAllowedTo.DoesNotExist:
        not_allowed = False
        
    print(not_allowed)

    if not_allowed:
        return Response({'Response': 'This blog post is private'})

    data = BlogPostSerializer(post).data
    return Response(data)










@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_blog_post(request, pk):
    post = get_object_or_404(BlogPost, id=pk)

    if request.user != post.author:
        return Response({'error': 'You cannot edit this blog post'})

    resp = {'Response': 'Failed to update'}
    serializer = BlogPostSerializer(post, data=request.data)

    if serializer.is_valid():
        serializer.save()
        resp['Response'] = 'Updated successfully'
        return Response(data=resp)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_blog_post(request, pk):
    post = get_object_or_404(BlogPost, id=pk)
    resp = {'Response': 'Failed to delete'}

    if request.user == post.author and post.delete():
        resp['Response'] = 'Successfully deleted'
    
    return Response(resp)



from ip2geotools.databases.noncommercial import DbIpCity

@api_view(['GET'])
def get_country(request):

    address = request.META.get('HTTP_X_FORWARDED_FOR')

    if address:
        ip = str(address.split(',')[0])
        
    else:
        ip = request.META.get('REMOTE_ADDR')

    location = DbIpCity.get(ip, api_key="free").country    

    return Response({'Response': ip, 'location': location})
