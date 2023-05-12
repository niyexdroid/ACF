# Generated by Django 4.1.5 on 2023-01-12 16:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_alter_comment_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('volunteer_date', models.DateTimeField(default=datetime.datetime(2023, 1, 12, 17, 47, 59, 792621))),
            ],
        ),
    ]