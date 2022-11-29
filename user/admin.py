from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'second_name', 'email')
    exclude = ('reset_code')

admin.site.register(User)

