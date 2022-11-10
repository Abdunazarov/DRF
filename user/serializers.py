from dataclasses import field
from urllib import request
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True) # write_only hides it from showing in Response()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'name', 'second_name', 'password', 'password2')

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'Response': 'Passwords do not match'})

        email = self.validated_data['email']
        name = self.validated_data.get('name', 'Default name')        

        user = User.objects.create_user(email=email, name=name, pwd=password)

        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    new_password2 = serializers.CharField()


    def save(self, validated_data, user):
        correct_password = user.check_password(validated_data['old_password'])  

        if correct_password:
            if not validated_data['new_password'] == validated_data['new_password2']:
                raise serializers.ValidationError({'Error': 'Passwords do not match'})

            user.set_password(validated_data['new_password'])
            user.save()
            return user

        else:
            raise serializers.ValidationError({'Error': 'Old password is wrong'})



class UserUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    second_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('name', 'second_name')
        # extra_kwargs = {
        #     'name': {'required': False},
        #     'first_name': {'required': False}
        # }

    def update(self, validated_data, instance):
        instance.name = validated_data.get('name', instance.name)
        instance.second_name = validated_data.get('second_name', instance.second_name)

        instance.save()
        return instance







        


        