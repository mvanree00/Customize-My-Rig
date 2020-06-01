# Generated by Django 3.0.6 on 2020-06-01 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CASE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('price', models.FloatField()),
                ('size', models.CharField(max_length=10)),
                ('links', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='FAN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('price', models.FloatField()),
                ('links', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='MOBO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('price', models.FloatField()),
                ('chipset', models.CharField(max_length=50)),
                ('links', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AddField(
            model_name='cpu',
            name='links',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cpu',
            name='manufacturer',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cpu',
            name='name',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gpu',
            name='links',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mem',
            name='links',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mem',
            name='name',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pwr',
            name='links',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pwr',
            name='name',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='storage',
            name='links',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='storage',
            name='name',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]