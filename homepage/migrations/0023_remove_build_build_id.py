# Generated by Django 3.0.8 on 2020-07-23 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0022_build'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='build',
            name='build_ID',
        ),
    ]
