# Generated by Django 4.0.4 on 2022-05-07 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rated',
            field=models.BooleanField(default=False),
        ),
    ]
