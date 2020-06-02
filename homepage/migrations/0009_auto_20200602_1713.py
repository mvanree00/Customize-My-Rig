# Generated by Django 3.0.6 on 2020-06-02 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0008_auto_20200602_0037'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='img',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cpu',
            name='img',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='fan',
            name='img',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='gpu',
            name='img',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='mem',
            name='img',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='mobo',
            name='img',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='pwr',
            name='img',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='storage',
            name='img',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='links',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='cpu',
            name='links',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='fan',
            name='links',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='gpu',
            name='links',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='mem',
            name='links',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='mobo',
            name='links',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='pwr',
            name='links',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='storage',
            name='capacity',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='storage',
            name='links',
            field=models.CharField(max_length=50, null=True),
        ),
    ]