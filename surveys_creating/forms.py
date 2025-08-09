from django import forms

from surveys_creating.models import Questionnaire, Question


class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ('name', 'author', 'email', 'min_scores')

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('number', 'question_text', 'question_obligation', 'choices')
