from django.db import models

class FeedPost(models.Model):
    id = models.AutoField('Идентификатор', primary_key=True)
    profile_id = models.IntegerField('Идентификатор профиля')
    blogpost_id = models.IntegerField('Идентификатор поста блога')
    is_read = models.BooleanField('Прочитано')

    def __init__(self, profile_id: int, blogpost_id: int, is_read: bool):
        super().__init__()

        self.profile_id = profile_id
        self.blogpost_id = blogpost_id
        self.is_read = is_read

    class Meta:
        verbose_name = 'Пост ленты'
        verbose_name_plural = 'Посты ленты'
