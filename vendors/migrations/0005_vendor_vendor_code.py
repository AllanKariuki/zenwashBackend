# Generated by Django 4.2.10 on 2024-03-27 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0004_serviceimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='vendor_code',
            field=models.CharField(editable=False, max_length=100, null=True, unique=True),
        ),
    ]
