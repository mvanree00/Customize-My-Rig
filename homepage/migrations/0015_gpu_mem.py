# Generated by Django 3.0.6 on 2020-06-19 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0014_auto_20200612_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='gpu',
            name='mem',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]