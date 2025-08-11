from django import forms

from surveys_creating.models import Question, Choice, Questionnaire


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ( 'choice_text', 'choice_points')


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text', 'question_obligation', 'active')

class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ('name', 'email', 'min_scores')
        readonly_fields = ('q_id', 'author')






