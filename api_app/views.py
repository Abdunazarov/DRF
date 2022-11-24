from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from django.shortcuts import get_object_or_404

from .models import *
from .serializers import *

from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def create_navabar(request):

    serializer = NavbarSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_all_navbars(request):
    print(request.META['LANGUAGE_CODE'])
    all = Navbar.objects.all()

    serializer = NavbarSerializer(all, many=True)

    return Response(serializer.data)  
    

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def create_navabar_child(request):

    serializer = NavbarChildSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(request.data)
        return Response(serializer.data)

    return Response(serializer.errors)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_all_navbar_childs(request):
    all = NavbarChild.objects.all()

    serializer = NavbarChildSerializer(all, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def test(request, account_pk):
    account = Account.objects.get(id=account_pk)
    account_allowed_users = account.allowed_users.all()


    if request.user in account_allowed_users:
        return Response({'Response': 'You are allowed to see this account'})
    
    return Response({'Response': 'This account is private'})
    

    
    