# Generated by Django 3.2.9 on 2024-09-06 11:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminAuthToken',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique token identifier', primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=50)),
                ('platform', models.CharField(max_length=50, null=True)),
                ('expiry_date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AuthToken',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique token identifier', primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=50)),
                ('platform', models.CharField(max_length=50, null=True)),
                ('expiry_date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BlackListedToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=500)),
            ],
        ),
    ]
