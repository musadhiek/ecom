# Generated by Django 3.1.2 on 2020-11-16 04:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0013_auto_20201116_0437'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='vendor',
        ),
    ]
