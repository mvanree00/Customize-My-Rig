# Generated by Django 3.0.6 on 2020-06-19 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0015_gpu_mem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpu',
            name='manufacturer',
            field=models.CharField(max_length=50),
        ),
    ]
