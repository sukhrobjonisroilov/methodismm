# Generated by Django 4.2.5 on 2023-10-07 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otptoken',
            name='by',
        ),
    ]