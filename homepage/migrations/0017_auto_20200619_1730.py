# Generated by Django 3.0.6 on 2020-06-19 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0016_auto_20200619_0144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cpu',
            name='price',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='fan',
            name='img',
            field=models.CharField(max_length=110, null=True),
        ),
    ]
