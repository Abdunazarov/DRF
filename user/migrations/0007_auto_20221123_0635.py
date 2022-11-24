# Generated by Django 3.2 on 2022-11-23 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_user_allowed_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='allowed_users',
        ),
        migrations.AddField(
            model_name='user',
            name='blocked_users',
            field=models.ManyToManyField(blank=True, null=True, related_name='blocked_users', to='user.Account'),
        ),
    ]
