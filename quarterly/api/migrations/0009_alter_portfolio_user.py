# Generated by Django 4.0.4 on 2022-05-16 00:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0008_alter_asset_holdings_alter_historicalasset_holdings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
