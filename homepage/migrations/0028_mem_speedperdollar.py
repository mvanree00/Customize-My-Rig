# Generated by Django 3.0.8 on 2020-07-29 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0027_mem_realspeed'),
    ]

    operations = [
        migrations.AddField(
            model_name='mem',
            name='speedperdollar',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
