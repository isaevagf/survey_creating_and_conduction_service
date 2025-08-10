from django import forms

from surveys_creating.models import Questionnaire, Question, Choice

class QuestionnaireForm(forms.ModelForm):
    choice = forms.ModelChoiceField(queryset=Question.objects.all())
    class Meta:
        model = Questionnaire
        fields = ('name', 'author')

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text', 'question_obligation')

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ( 'choice_text', 'choice_points')
