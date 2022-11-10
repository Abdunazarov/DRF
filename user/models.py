from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# creating a custom user, where email would be unique filed and the user will not have username field
class UserManager(BaseUserManager):

    def create_user(self, email, name, pwd, **extra_fields): # extra_fields are is_admin, is_staff...
        email = self.normalize_email(email) # self indicates to BaseUserManger
        user = self.model(email=email, name=name)
        user.set_password(pwd)
        user.save()
        return user # try without return
    
    def create_superuser(self, email, name, password, **extra_fields):
        user = self.create_user(email=email, name=name, pwd=password, **extra_fields)
        user.is_admin = user.is_active = user.is_staff = user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    second_name = models.CharField(max_length=200, blank=True)

    is_staff = models.BooleanField(default=False) # whether this user can access the admin
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False) # why is_admin if there's is_staff? (!)    
    last_login = models.DateTimeField(auto_now=True) # auto_now - saves the date every time the object is saved  
    date_joined = models.DateTimeField(auto_now_add=True)  # auto_now_add - saves the date when the object is created

    objects = UserManager()

    USERNAME_FIELD = 'email' # unique identifier ?
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    # study django permission in depth (!)
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
        


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_account(sender, instance=None, created=False, **kwargs):
    if created:
        Account.objects.create(user=instance)



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



