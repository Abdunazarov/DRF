from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from .models import Account

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated



@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    data = {}

    if serializer.is_valid():
        user = serializer.save()
        data['email'] = user.email
        data['name'] = user.name
        data['password'] = request.data['password']
        data['token'] = Token.objects.get(user=user).key # because token in itself returns an object and the obj is not JSON serializable :)
        
        return Response(data)

    return Response(serializer.errors)


# @api_view(['GET'])
# def list_user(request):
#     users = User.objects.all()

#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data)
    
from rest_framework.generics import ListAPIView
from rest_framework import filters


class ListUserView(ListAPIView):
    search_fields = ['name', 'second_name', 'email']
    filter_backends = (filters.SearchFilter,)
    queryset = User.objects.all()
    serializer_class = UserSerializer



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = User.objects.get(email=request.user)

    serializer = UserSerializer(user)

    return Response(serializer.data)
    

from django.contrib.auth import logout


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    data = {'Response': 'Failed to log out'}
    token = Token.objects.get(user=request.user.id)

    if token.delete():
        logout(request)
        data['Response'] = 'Successfully logged out'

    return Response(data)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user

    serializer = UserUpdateSerializer(instance=user, data=request.data)

    if serializer.is_valid():
        updated_user = serializer.update(request.data, user)
        data = UserSerializer(updated_user).data
        return Response(data)

    return Response(serializer.errors)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    data = {'Response': 'Failed to updated password'}

    serializers = PasswordChangeSerializer(user, data=request.data)

    if serializers.is_valid():
        serializers.save(request.data, user)
        data['Response'] = 'Successfully updated'
        return Response(data)

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_account(request, user_viewed_pk):
    user_viewed = Account.objects.get(id=user_viewed_pk).user
    user = request.user

    if user_viewed.private == True:
        account_followers = user_viewed.followers.all()
        if Account.objects.get(user=user) in account_followers:
            data = UserSerializer(user_viewed).data
            return Response(data)

        return Response({"Response": "This account is private"})
    
    data = UserSerializer(user_viewed).data
    return Response(data)





