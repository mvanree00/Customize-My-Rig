# Generated by Django 3.0.6 on 2020-06-13 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0013_auto_20200612_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storage',
            name='capacity',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
