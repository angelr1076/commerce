# Generated by Django 3.1 on 2020-12-24 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0039_auto_20201220_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='starting_price',
            field=models.DecimalField(decimal_places=3, default=1.0, max_digits=10),
        ),
    ]