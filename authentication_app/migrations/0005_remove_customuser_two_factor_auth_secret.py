# Generated by Django 4.2.16 on 2024-11-05 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_app', '0004_rename_mfa_enabled_customuser_is_2fa_enabled_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='two_factor_auth_secret',
        ),
    ]
