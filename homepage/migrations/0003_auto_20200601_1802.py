# Generated by Django 3.0.6 on 2020-06-01 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_auto_20200601_0143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cpu',
            name='manufacturer',
        ),
        migrations.AddField(
            model_name='storage',
            name='kind',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cpu',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='storage',
            name='form',
            field=models.CharField(max_length=20),
        ),
    ]