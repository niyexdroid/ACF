# Generated by Django 4.1.5 on 2023-01-12 16:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_volunteer'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsLetterMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='volunteer_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 12, 17, 49, 34, 348386)),
        ),
    ]
