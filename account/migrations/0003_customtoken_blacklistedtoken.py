# Generated by Django 4.2.10 on 2024-03-19 17:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_userprofile_image_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomToken',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Key')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='authentication_token', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'CustomToken',
                'verbose_name_plural': 'CustomTokens',
            },
        ),
        migrations.CreateModel(
            name='BlackListedToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=500)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='token_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('token', 'user')},
            },
        ),
    ]