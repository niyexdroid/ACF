# Generated by Django 4.1.6 on 2023-05-05 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_category_comment_post_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-last_modified', '-creation_date']},
        ),
        migrations.AddField(
            model_name='post',
            name='url_aware_title',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='label',
            field=models.CharField(choices=[('Health', 'Health'), ('Diet', 'Diet'), ('Lifestyle', 'Lifestyle')], max_length=200, unique=True),
        ),
    ]
