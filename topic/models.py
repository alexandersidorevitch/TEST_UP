from django.db import models

# Create your models here.
from django.urls import reverse


class Topics(models.Model):
    topic = models.CharField(max_length=256, verbose_name='Тема')

    def __str__(self):
        return f' {self.topic}'

    class Meta:
        verbose_name = 'тема'
        verbose_name_plural = 'темы'

    def get_absolute_url(self):
        return reverse('topic:question', args=[self.id])


class Types(models.Model):
    type = models.CharField(max_length=256, verbose_name='Тип')

    def __str__(self):
        return f' {self.type}'

    class Meta:
        verbose_name = 'тип'
        verbose_name_plural = 'типы'


class Questions(models.Model):
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE, blank=True, null=True, default=None,
                              verbose_name='Тема', )
    question = models.TextField(verbose_name='Вопрос', blank=True, null=True, default=None)
    type = models.ForeignKey(Types, on_delete=models.CASCADE, blank=True, null=True, default=None,
                             verbose_name='Тип вопроса', )
    hint = models.CharField(max_length=256, verbose_name='Подсказка')
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f' {self.question}'

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'


class Answers(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                 verbose_name='Вопрос')
    answer = models.CharField(max_length=256, verbose_name='Ответ')
    is_right = models.BooleanField(verbose_name='Правильный ответ', default=False, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f' {self.answer}'

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'

    def save(self, *args, **kwargs):
        if (self.is_right and self.question.type.type == 'OneChoice') or (
                not self.is_right and self.question.type.type == 'TextField'):
            try:

                if self.question.type.type == 'OneChoice':
                    answer = Answers.objects.get(question=self.question, is_right=True)
                    answer.is_right = False
                    answer.save()
                else:
                    self.is_right = True
            except models.ObjectDoesNotExist:
                pass

        super(Answers, self).save(*args, **kwargs)
