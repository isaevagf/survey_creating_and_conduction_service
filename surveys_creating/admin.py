from .models import Questionnaire, Question, Choice
from django.contrib import admin

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    readonly_fields = ('questionnaire', 'number')

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0
    readonly_fields = ('question', 'number')

@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'email', 'min_scores')
    list_filter = ('author', 'min_scores')
    search_fields = ('user__username',)
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'question_obligation', 'active')
    list_filter = ('questionnaire',)
    search_fields = ('question_text',)
    inlines = [ChoiceInline]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'choice_points')
    list_filter = ('question',)
    search_fields = ('choice_text',)