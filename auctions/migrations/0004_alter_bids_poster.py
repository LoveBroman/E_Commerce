# Generated by Django 4.2.2 on 2023-07-04 12:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_listing_poster_listing_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='poster',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
