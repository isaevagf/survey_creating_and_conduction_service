from .models import Questionnaire, Question, Choice
from django.contrib import admin

class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'email', 'min_scores')
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Question)
admin.site.register(Choice)