from django.db import models
from django.contrib.auth import get_user_model
from surveys_creating.models import Questionnaire, Question, Choice


class Response(models.Model):
    questionnaire = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE, verbose_name="Анкета"
    )
    user = models.ForeignKey(
        get_user_model(), null=True, blank=True,
        on_delete=models.SET_NULL, verbose_name="Пользователь"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('questionnaire', 'user')
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return f"Ответ {self.user} на {self.questionnaire}"


class Answer(models.Model):
    response = models.ForeignKey(
        Response, related_name="answers", on_delete=models.CASCADE
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text_answer = models.TextField(blank=True, null=True)
    choice = models.ForeignKey(
        Choice, blank=True, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = "Ответ на вопрос"
        verbose_name_plural = "Ответы на вопросы"

    def __str__(self):
        return f"Ответ на '{self.question}'"