from urllib import request
from rest_framework import serializers
from .models import User, Account

from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
import string
import random


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    password2 = serializers.CharField(write_only=True) # write_only hides it from showing in Response()
    password = serializers.CharField(write_only=True)
    followers = serializers.StringRelatedField(many=True, read_only=True) # returns the __str__ method of the object
    followings = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'second_name', 'password', 'password2', 'private', 'followers', 'followings')

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
    follower_remove = serializers.CharField(required=False)
    follow = serializers.CharField(required=False)
    private = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('name', 'second_name', 'follower_remove', 'follow', 'private')
        # extra_kwargs = {
        #     'name': {'required': False},
        #     'first_name': {'required': False}
        # }


    def update(self, validated_data, instance):
        instance.name = validated_data.get('name', instance.name)
        instance.second_name = validated_data.get('second_name', instance.second_name)
        instance.private = validated_data.get('private', instance.private)

        if validated_data.get('follow'):
            instance_account = Account.objects.get(user=instance)
            follow = get_object_or_404(User, email=validated_data['follow'])
            follow_account = Account.objects.get(user=follow.id)


            follow.followers.all = follow.followers.add(instance_account)
            instance.followings.all = instance.followings.add(follow_account)

        if validated_data.get('unfollow'):
            instance_account = Account.objects.get(user=instance)
            unfollow_user = get_object_or_404(User, email=validated_data['unfollow'])
            unfollow_account = Account.objects.get(user=unfollow_user.id)

            unfollow_user.followers.all = unfollow_user.followers.remove(instance_account)
            instance.followings.all = instance.followings.remove(unfollow_account)

        if validated_data.get('follower_remove'):
            user = get_object_or_404(User, email=validated_data['follower_remove']).id
            follower = Account.objects.get(user=user)

            instance.followers.all = instance.followers.remove(follower)
        

        instance.save()
        return instance

# send 4-digit code to email
# enter that code to form, if matches, give permission to change password
# enter new password (new_password, new_password2)
 

class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=4)
    
    def validate_and_send(self, request_data):
        exists = User.objects.filter(email=request_data['email']).exists()
        if exists == False:
            raise serializers.ValidationError({'Error': 'This user does not exist'})


        chars = string.ascii_letters + string.digits
        code = ''.join(random.choices(chars, k=5))
        subject = "Password reset"
        message = f'''<h3 style="color:black; font-weight:500;">Please enter the following 5-digit code in order to reset password for the user {request_data['email']}, by going to the link for <a href="http://localhost:8000/user/reset_password/">resetting password</a></h3>
                                                        <h1 style="color:red; margin: 0em 10em 0em 18em">{code}</h1>'''

        send_mail(
            subject=subject,
            message='',
            from_email="Don't Reply (DRF)",
            recipient_list=[request_data['email']],
            fail_silently=False,
            html_message=message
        )
        

        return code

class ResetPasswordSerializer(serializers.Serializer):
    reset_code = serializers.CharField()
    new_password = serializers.CharField()
    new_password2 = serializers.CharField()

    def check_save(self, request_data, code, user_email):
        user = User.objects.get(email=user_email)
        new_password = request_data['new_password']

        if not code == request_data['reset_code']:
            raise serializers.ValidationError({'Error': 'The reset code is incorrect!'})

        if not new_password == request_data['new_password2']:
            raise serializers.ValidationError({'Error': 'Password do not match!'})
        
        user.set_password(new_password)
        user.save()
        return user





