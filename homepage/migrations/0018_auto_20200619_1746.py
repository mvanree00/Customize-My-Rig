# Generated by Django 3.0.6 on 2020-06-19 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0017_auto_20200619_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='price',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='fan',
            name='price',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='gpu',
            name='price',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='mem',
            name='price',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='mobo',
            name='price',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='pwr',
            name='price',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='storage',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]