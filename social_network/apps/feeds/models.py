from django.db import models

class FeedPost(models.Model):
    id = models.AutoField('Идентификатор', primary_key=True)
    profile_id = models.IntegerField('Идентификатор профиля')
    blogpost_id = models.IntegerField('Идентификатор поста блога')
    is_read = models.BooleanField('Прочитано')

    class Meta:
        verbose_name = 'Пост ленты'
        verbose_name_plural = 'Посты ленты'
