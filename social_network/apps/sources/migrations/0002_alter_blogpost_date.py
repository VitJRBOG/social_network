# Generated by Django 4.0.4 on 2022-05-18 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='date',
            field=models.CharField(max_length=20, verbose_name='Дата создания'),
        ),
    ]
