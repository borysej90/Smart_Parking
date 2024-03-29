# Generated by Django 3.1.6 on 2021-02-17 09:32

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParkingSite',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=100)),
                ('lots_number', models.IntegerField()),
                ('cameras_number', models.IntegerField()),
                ('is_free', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='VideoProcessorType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type_name', models.CharField(max_length=50)),
                ('image_url', models.CharField(max_length=100)),
                ('tag', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='VideoProcessor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('stream_url', models.CharField(max_length=100)),
                ('parking_site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.parkingsite')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.videoprocessortype')),
            ],
        ),
        migrations.CreateModel(
            name='ParkingLot',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('coordinates', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('is_occupied', models.BooleanField()),
                ('parking_site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.parkingsite')),
            ],
        ),
    ]
