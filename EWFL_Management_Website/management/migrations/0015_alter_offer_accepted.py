# Generated by Django 5.1.2 on 2024-11-26 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0014_offer_accepted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='accepted',
            field=models.CharField(default='pending', max_length=10),
        ),
    ]
