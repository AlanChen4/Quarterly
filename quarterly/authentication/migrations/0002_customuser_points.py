# Generated by Django 4.0.4 on 2022-05-07 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='points',
            field=models.PositiveIntegerField(default=100),
            preserve_default=False,
        ),
    ]
