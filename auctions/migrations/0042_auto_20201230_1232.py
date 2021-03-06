# Generated by Django 3.1 on 2020-12-30 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0041_auto_20201224_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('misc', 'misc'), ('computers', 'computers'), ('toys', 'toys'), ('pets', 'pets'), ('beauty', 'beauty'), ('video games', 'video games'), ('auto', 'auto'), ('clothing', 'clothing')], default='misc', max_length=30),
        ),
        migrations.AlterField(
            model_name='listing',
            name='current_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
