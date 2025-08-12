import uuid

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Questionnaire(models.Model):
    q_id = models.IntegerField(unique=True, primary_key=True, db_index=True, editable=False)
    name = models.CharField("Наименование анкеты")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    max_questions = models.IntegerField("Максимальное количество ответов на 1 вопрос")

    def __str__(self):
        return self.name

class Question(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, null=True)
    number = models.IntegerField(unique=True, primary_key=True, db_index=True, editable=False)
    question_text = models.TextField("Текст вопроса", max_length=200)
    active = models.BooleanField("Активный", default=True)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    number = models.IntegerField(unique=True, primary_key=True, db_index=True, editable=False)
    choice_text = models.TextField("Текст ответа", max_length=200)
    choice_points = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text



