# Generated by Django 4.0.4 on 2022-05-11 20:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_historicalreview_overall_rating_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalportfolio',
            name='risk_tolerance',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='historicalportfolio',
            name='time_horizon',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='risk_tolerance',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='time_horizon',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='historicalportfolio',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Additional Information'),
        ),
        migrations.AlterField(
            model_name='historicalreview',
            name='overall_rating',
            field=models.IntegerField(blank=True, choices=[(1, 'Recommend significant changes'), (2, 'Recommend moderate changes'), (3, 'Recommend minor changes'), (4, 'Recommend little to no change'), (5, 'Recommend no change')], null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Overall Appropriateness'),
        ),
        migrations.AlterField(
            model_name='historicalreview',
            name='risk_rating',
            field=models.IntegerField(blank=True, choices=[(1, 'Recommend significant changes'), (2, 'Recommend moderate changes'), (3, 'Recommend minor changes'), (4, 'Recommend little to no change'), (5, 'Recommend no change')], null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Risk Level'),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Additional Information'),
        ),
        migrations.AlterField(
            model_name='review',
            name='overall_rating',
            field=models.IntegerField(blank=True, choices=[(1, 'Recommend significant changes'), (2, 'Recommend moderate changes'), (3, 'Recommend minor changes'), (4, 'Recommend little to no change'), (5, 'Recommend no change')], null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Overall Appropriateness'),
        ),
        migrations.AlterField(
            model_name='review',
            name='risk_rating',
            field=models.IntegerField(blank=True, choices=[(1, 'Recommend significant changes'), (2, 'Recommend moderate changes'), (3, 'Recommend minor changes'), (4, 'Recommend little to no change'), (5, 'Recommend no change')], null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Risk Level'),
        ),
    ]
