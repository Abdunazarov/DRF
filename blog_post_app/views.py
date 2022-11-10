from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from django.shortcuts import get_object_or_404

from .models import *
from .serializers import *

from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import ListAPIView
from rest_framework import filters

from django.shortcuts import render
from api_app.models import ViewCount


class BlogPostListView(ListAPIView):
    search_fields = ['text', 'author__email'] # ForeignKey or ManyToMany field should be filterd this way!
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


from .get_language import get_language


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def detail_blog_post(request, pk):

    post = get_language(lan=request.LANGUAGE_CODE, pk=pk)
    comments = []
    all_comments = BlogPostComments.objects.filter(post=post)
    for comment in all_comments:
        comments.append(comment.id)


    data = BlogPostSerializer(post).data
    data['comments'] = comments

    if post == None:
        return Response({'Error': 'No such blog post'})

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




# @api_view(['POST'])
def create_blog_front(request):
    notification = False

    if request.method == 'POST':
        BlogPost.objects.create(
            author=User.objects.get(id=1),
            text=request.POST['post_text'], 
            image=request.POST.get('post_image')
        )
        notification = True


    return render(request, 'api_app/create_blog.html', {'notification': notification})



@api_view(['GET'])
def visitors_count(request):
    user = request.user

    address = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = 'LOX'

    if address:
        ip = str(address.split(',')[0])

    else:
        ip = request.META.get('REMOTE_ADDR')

    return Response({'Response': ip})
