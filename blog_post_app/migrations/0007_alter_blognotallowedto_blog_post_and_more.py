# Generated by Django 4.1 on 2022-11-09 08:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog_post_app', '0006_remove_blogpostrus_private_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blognotallowedto',
            name='blog_post',
            field=models.ManyToManyField(to='blog_post_app.blogpost'),
        ),
        migrations.AlterField(
            model_name='blognotallowedto',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
