from django.db import models
from user.models import User

# Navbar
class Navbar(models.Model):
    navbar_name = models.CharField(max_length=100)

    def __str__(self):
        return self.navbar_name


class NavbarChild(models.Model):
    navbar_child_name = models.CharField(max_length=100)
    navbar = models.ForeignKey(Navbar, on_delete=models.CASCADE)

    def __str__(self):
        return self.navbar_child_name



class ViewCount(models.Model):
    country = models.CharField(max_length=100)

    user = models.ForeignKey(User, on_delete=models.CASCADE)



    def __str__(self):
        return self.user.email

