# Generated by Django 4.0.4 on 2022-05-12 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_customuser_points_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='historicalcustomuser',
            name='dob',
        ),
        migrations.AddField(
            model_name='customuser',
            name='display_name',
            field=models.CharField(max_length=255, null=True, unique=True, verbose_name='username'),
        ),
        migrations.AddField(
            model_name='historicalcustomuser',
            name='display_name',
            field=models.CharField(db_index=True, max_length=255, null=True, verbose_name='username'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='historicalcustomuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='historicalcustomuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]