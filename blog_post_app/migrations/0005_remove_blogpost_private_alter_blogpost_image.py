# Generated by Django 4.1 on 2022-11-09 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_post_app', '0004_rename_comment_blogpostcomments_body_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='private',
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(default=None, upload_to=''),
        ),
    ]
