# Generated by Django 3.1.2 on 2020-11-08 03:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_vendor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='vendor',
        ),
    ]
