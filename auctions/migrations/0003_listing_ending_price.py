# Generated by Django 3.1 on 2020-12-04 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='ending_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]