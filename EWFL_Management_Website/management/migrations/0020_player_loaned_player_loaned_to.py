# Generated by Django 5.1.2 on 2024-12-14 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0019_offer_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='loaned',
            field=models.CharField(default='N/A', max_length=5),
        ),
        migrations.AddField(
            model_name='player',
            name='loaned_to',
            field=models.CharField(default='N/A', max_length=64),
        ),
    ]
