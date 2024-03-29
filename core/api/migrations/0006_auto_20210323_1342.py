# Generated by Django 3.1.6 on 2021-03-23 11:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210323_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingsite',
            name='latitude',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(-90, 'Limit error'), django.core.validators.MaxValueValidator(90, 'Limit error')]),
        ),
        migrations.AlterField(
            model_name='parkingsite',
            name='longitude',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(-180, 'Limit error'), django.core.validators.MaxValueValidator(180, 'Limit error')]),
        ),
    ]
