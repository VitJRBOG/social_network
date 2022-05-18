# Generated by Django 4.0.4 on 2022-05-18 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('profile_id', models.IntegerField(verbose_name='Идентификатор профиля')),
                ('blog_id', models.IntegerField(verbose_name='Идентификатор блога')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('name', models.CharField(max_length=256, verbose_name='Полное имя')),
                ('login', models.CharField(max_length=25, verbose_name='Имя пользователя')),
                ('password_hash', models.CharField(max_length=256, verbose_name='Хэш пароля')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
    ]