# Generated by Django 3.0.6 on 2020-06-02 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0007_auto_20200602_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='links',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='fan',
            name='links',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='mobo',
            name='links',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='pwr',
            name='links',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='storage',
            name='links',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]