# Generated by Django 3.1 on 2020-12-06 02:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20201206_0239'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='user_watching',
            new_name='user',
        ),
    ]