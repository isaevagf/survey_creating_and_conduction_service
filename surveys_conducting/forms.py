from django import forms
from surveys_creating.models import Choice


class SurveyResponseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)

        for question in questions:
            required = question.question_obligation
            choice_qs = Choice.objects.filter(question=question)

            if not choice_qs.exists():
                # Текстовый ответ
                self.fields[f"question_{question.pk}"] = forms.CharField(
                    label=question.question_text,
                    required=required
                )
            elif choice_qs.count() == 1:
                # radio-button for 1 choice
                self.fields[f"question_{question.pk}"] = forms.ChoiceField(
                    label=question.question_text,
                    widget=forms.RadioSelect,
                    choices=[(c.pk, c.choice_text) for c in choice_qs],
                    required=required
                )
            else:
                # check-box multiple choice
                self.fields[f"question_{question.pk}"] = forms.MultipleChoiceField(
                    label=question.question_text,
                    widget=forms.CheckboxSelectMultiple,
                    choices=[(c.pk, c.choice_text) for c in choice_qs],
                    required=required
                )