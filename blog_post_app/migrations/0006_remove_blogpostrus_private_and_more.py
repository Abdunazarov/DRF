# Generated by Django 4.1 on 2022-11-09 08:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog_post_app', '0005_remove_blogpost_private_alter_blogpost_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpostrus',
            name='private',
        ),
        migrations.RemoveField(
            model_name='blognotallowedto',
            name='blog_post',
        ),
        migrations.RemoveField(
            model_name='blognotallowedto',
            name='user',
        ),
        migrations.AddField(
            model_name='blognotallowedto',
            name='blog_post',
            field=models.ManyToManyField(blank=True, null=True, to='blog_post_app.blogpost'),
        ),
        migrations.AddField(
            model_name='blognotallowedto',
            name='user',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
