# Generated by Django 3.1.3 on 2020-11-26 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0011_auto_20201126_0839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='pic1',
            field=models.ImageField(default=0, upload_to='images/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='pic2',
            field=models.ImageField(default=0, upload_to='images/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='pic3',
            field=models.ImageField(default=0, upload_to='images/'),
            preserve_default=False,
        ),
    ]
