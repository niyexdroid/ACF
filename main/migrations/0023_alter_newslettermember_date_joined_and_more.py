# Generated by Django 4.1.5 on 2023-01-12 19:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_alter_event_options_alter_newslettermember_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newslettermember',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 12, 20, 1, 27, 371318)),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='volunteer_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 12, 20, 1, 27, 355694)),
        ),
    ]