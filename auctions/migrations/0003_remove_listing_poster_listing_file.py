# Generated by Django 4.2.2 on 2023-07-04 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing_description_listing_image_alter_user_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='poster',
        ),
        migrations.AddField(
            model_name='listing',
            name='file',
            field=models.FileField(null=True, upload_to='uploads/'),
        ),
    ]
