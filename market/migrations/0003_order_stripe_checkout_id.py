# Generated by Django 5.2.1 on 2025-05-22 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='stripe_checkout_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
