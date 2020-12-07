# Generated by Django 3.1.3 on 2020-11-25 07:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_restaurant_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='description',
            field=models.CharField(max_length=500, validators=[django.core.validators.MinLengthValidator(2, 'Name must be greater than 2 characters')]),
        ),
    ]
