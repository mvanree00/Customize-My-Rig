# Generated by Django 3.0.8 on 2020-07-24 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0024_auto_20200723_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='build',
            name='EXTRA_links',
            field=models.CharField(max_length=50, null=True),
        ),
    ]