# Generated by Django 4.2.10 on 2024-02-19 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='location',
        ),
    ]