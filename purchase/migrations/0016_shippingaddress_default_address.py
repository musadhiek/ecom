# Generated by Django 3.1.2 on 2020-11-19 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0015_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='default_address',
            field=models.BooleanField(default=False),
        ),
    ]
