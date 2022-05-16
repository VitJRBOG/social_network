from django.db import models

class Blog(models.Model):
    id = models.AutoField('Идентификатор', primary_key=True)
    profile_id = models.IntegerField('Идентификатор профиля')

    def __init__(self, profile_id: int):
        super().__init__()

        self.profile_id = profile_id

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'


class BlogPost(models.Model):
    id = models.AutoField('Идентификатор', primary_key=True)
    blog_id = models.IntegerField('Идентификатор блога')

    def __init__(self, blog_id: int):
        super().__init__()

        self.blog_id = blog_id

    class Meta:
        verbose_name = 'Пост блога'
        verbose_name_plural = 'Посты блога'
