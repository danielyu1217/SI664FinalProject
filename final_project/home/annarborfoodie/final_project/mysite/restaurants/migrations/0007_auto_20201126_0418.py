# Generated by Django 3.1.3 on 2020-11-26 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0006_auto_20201126_0305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='description',
            field=models.TextField(),
        ),
    ]
