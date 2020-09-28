from django.db import models


# Create your models here.


class Users(models.Model):
    name = models.CharField(max_length=256, verbose_name='Имя', null=False, default='')
    group = models.CharField(max_length=10, verbose_name='Группа', null=False, default='')
    session = models.CharField(max_length=256, verbose_name='Сессия', null=False, default='')

    def __str__(self):
        return f'{self.name} {self.session}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
