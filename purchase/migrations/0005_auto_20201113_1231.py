# Generated by Django 3.1.2 on 2020-11-13 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0004_shippingaddress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='pincode',
            field=models.CharField(max_length=6, null=True),
        ),
    ]
