from re import M
from wsgiref import validate
from rest_framework import serializers
from .models import *


class NavbarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Navbar
        fields = ('id', 'navbar_name',)


class NavbarChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavbarChild
        fields = ('id', 'navbar_child_name', 'navbar')


    def save(self, validated_data):
        nav_child = NavbarChild(
            navbar_child_name=validated_data['navbar_child_name'],
            navbar=Navbar.objects.get(pk=validated_data['navbar'])
        )

        nav_child.save()
        return nav_child
        
