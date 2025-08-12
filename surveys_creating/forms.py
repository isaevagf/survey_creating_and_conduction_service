from django import forms

from surveys_creating.models import Question, Choice, Questionnaire


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ( 'choice_text', 'choice_points')


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text', 'active')
        readonly_fields = ('number')

class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ('name', 'max_questions')




