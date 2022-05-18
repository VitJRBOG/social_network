from django.db import models

class Profile(models.Model):
    id = models.AutoField('Идентификатор', primary_key=True)
    name = models.CharField('Полное имя', max_length=256)
    login = models.CharField('Имя пользователя', max_length=25)
    password_hash = models.CharField('Хэш пароля', max_length=256)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Following(models.Model):
    id = models.AutoField('Идентификатор', primary_key=True)
    profile_id = models.IntegerField('Идентификатор профиля')
    blog_id = models.IntegerField('Идентификатор блога')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
