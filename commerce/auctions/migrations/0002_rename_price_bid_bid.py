# Generated by Django 4.2.3 on 2023-08-20 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='price',
            new_name='bid',
        ),
    ]
