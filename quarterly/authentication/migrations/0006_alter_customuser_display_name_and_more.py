# Generated by Django 4.0.4 on 2022-05-12 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_remove_customuser_dob_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='display_name',
            field=models.CharField(default='<django.db.models.fields.EmailField>', max_length=255, null=True, unique=True, verbose_name='username'),
        ),
        migrations.AlterField(
            model_name='historicalcustomuser',
            name='display_name',
            field=models.CharField(db_index=True, default='<django.db.models.fields.EmailField>', max_length=255, null=True, verbose_name='username'),
        ),
    ]
