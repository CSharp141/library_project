# Generated by Django 4.2.7 on 2023-11-24 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_users_password_alter_users_username'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Users',
        ),
    ]
