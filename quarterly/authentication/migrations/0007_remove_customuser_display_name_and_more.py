# Generated by Django 4.0.4 on 2022-05-12 23:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_alter_customuser_display_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='display_name',
        ),
        migrations.RemoveField(
            model_name='historicalcustomuser',
            name='display_name',
        ),
    ]