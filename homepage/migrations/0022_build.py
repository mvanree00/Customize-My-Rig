# Generated by Django 3.0.8 on 2020-07-23 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0021_auto_20200715_1622'),
    ]

    operations = [
        migrations.CreateModel(
            name='BUILD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('build_ID', models.IntegerField(null=True)),
                ('CPU_links', models.CharField(max_length=50, null=True)),
                ('GPU_links', models.CharField(max_length=50, null=True)),
                ('MEM_links', models.CharField(max_length=50, null=True)),
                ('STORAGE_links', models.CharField(max_length=50, null=True)),
                ('PWR_links', models.CharField(max_length=50, null=True)),
                ('MOBO_links', models.CharField(max_length=50, null=True)),
                ('FAN_links', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]
