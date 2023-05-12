# Generated by Django 4.2 on 2023-04-15 09:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_alter_cause_event_date_alter_contactor_contact_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cause',
            name='creation_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='creation_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='contactor',
            name='contact_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='donation',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='donator',
            name='creation_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='creation_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='newslettermember',
            name='date_joined',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='date_added',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='volunteer_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 15, 10, 9, 41, 934404)),
        ),
    ]