# Generated by Django 4.0.4 on 2022-05-11 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_historicalcustomuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='points',
            field=models.PositiveIntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='historicalcustomuser',
            name='points',
            field=models.PositiveIntegerField(default=100),
        ),
    ]
