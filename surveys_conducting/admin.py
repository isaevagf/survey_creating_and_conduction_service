from django.contrib import admin
from .models import Response, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ('question', 'text_answer', 'choice')


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'questionnaire', 'user', 'created_at')
    list_filter = ('questionnaire', 'created_at')
    search_fields = ('user__username',)
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'response', 'question', 'text_answer', 'choice')
    list_filter = ('question',)
    search_fields = ('text_answer',)
