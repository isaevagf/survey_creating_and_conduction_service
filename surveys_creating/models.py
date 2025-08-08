from django.db import models
from django.contrib.auth.models import User

class Questionnaire(models.Model):
    name = models.CharField("Наименование анкеты")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField("Контактный почтовый адрес автора анкеты")
    min_scores = models.IntegerField("Общее количество  баллов по анкете, обязательное для отправки", help_text = "(0 - если нужно отправлять любую анкету)")

    def __str__(self):
        return self.name

class Question(models.Model):
    number = models.IntegerField("№ Порядковый номер вопроса", default=-1)
    question_text = models.CharField("Текст вопроса", max_length=200)
    question_obligation = models.BooleanField("Обязательность вопроса", default=False)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField("Текст ответа", max_length=200)
    choice_points = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text