# Generated by Django 4.0.4 on 2022-04-29 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_asset_id_alter_review_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='description',
            field=models.TextField(verbose_name='Review Description'),
        ),
    ]