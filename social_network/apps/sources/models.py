from django.db import models

class Blog(models.Model):
    id = models.AutoField('Идентификатор', primary_key=True)
    name = models.CharField('Название', max_length=256)
    profile_id = models.IntegerField('Идентификатор профиля')

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'


class BlogPost(models.Model):
    id = models.AutoField('Идентификатор', primary_key=True)
    title = models.CharField('Заголовок', max_length=50)
    text = models.TextField('Текст', max_length=140)
    date = models.IntegerField('Дата создания')
    blog_id = models.IntegerField('Идентификатор блога')

    class Meta:
        verbose_name = 'Пост блога'
        verbose_name_plural = 'Посты блога'
