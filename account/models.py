from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from topic.models import Topics


class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE, verbose_name='Тема')
    percent_of_correct = models.DecimalField(verbose_name='Процент правильных ответов', decimal_places=1, max_digits=5)
    time_for_ending = models.TimeField(verbose_name='Время прохождения', default='00:00')
    data = models.DateTimeField(verbose_name='Дата прохождения теста и время прохождения теста', auto_now=True)

    def __str__(self):
        return f'{self.user} {self.data}'

    class Meta:
        verbose_name = 'результат теста'
        verbose_name_plural = 'результаты тестов'
