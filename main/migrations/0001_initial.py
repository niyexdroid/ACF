# Generated by Django 4.1.4 on 2022-12-27 17:13

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cause',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='cause_images')),
                ('target_amount', models.IntegerField()),
                ('reached_amount', models.IntegerField()),
                ('creation_date', models.DateTimeField(default=datetime.datetime.today)),
            ],
        ),
        migrations.CreateModel(
            name='Commentor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, null=True)),
                ('image', models.ImageField(blank=True, upload_to='secondary_user_images')),
                ('creation_date', models.DateTimeField(default=datetime.datetime.today)),
            ],
        ),
        migrations.CreateModel(
            name='Donator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.IntegerField(null=True)),
                ('picture', models.ImageField(null=True, upload_to='user_images')),
                ('creation_date', models.DateTimeField(default=datetime.datetime.today)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('date', models.DateTimeField()),
                ('venue', models.CharField(max_length=1000)),
                ('image', models.ImageField(upload_to='event_images')),
                ('creation_date', models.DateTimeField(default=datetime.datetime.today)),
                ('cause', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='event', to='main.cause')),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('time', models.DateTimeField(default=datetime.datetime.today)),
                ('cause', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='donations', to='main.cause')),
                ('donator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='donations', to='main.donator')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=200)),
                ('creation_date', models.DateTimeField(default=datetime.datetime.today)),
                ('commentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='main.commentor')),
            ],
        ),
    ]
