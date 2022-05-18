from django.db import models

class Profile(models.Model):
    id = models.AutoField('Идентификатор', primary_key=True)
    name = models.CharField('Полное имя', max_length=256)

    def __init__(self, name: str):
        super().__init__()

        self.name = name

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Following(models.Model):
    id = models.AutoField('Идентификатор', primary_key=True)
    profile_id = models.IntegerField('Идентификатор профиля')
    blog_id = models.IntegerField('Идентификатор блога')

    def __init__(self, profile_id: int, blog_id: int):
        super().__init__()

        self.profile_id = profile_id
        self.blog_id = blog_id

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
