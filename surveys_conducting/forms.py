from django import forms
from surveys_creating.models import Choice


class SurveyResponseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)

        for question in questions:
            required = question.question_obligation
            choices = Choice.objects.filter(question=question)

            if not choices.exists():
                # Текстовый ответ
                self.fields[f"question_{question.id}"] = forms.CharField(
                    label=question.question_text,
                    required=required
                )
            else:
                if choices.count() == 1:
                    # radio-button 1 choice
                    self.fields[f"question_{question.id}"] = forms.ChoiceField(
                        label=question.question_text,
                        widget=forms.RadioSelect,
                        choices=[(c.id, c.choice_text) for c in choices],
                        required=required
                    )
                else:
                    # check-box multiple choice
                    self.fields[f"question_{question.id}"] = forms.MultipleChoiceField(
                        label=question.question_text,
                        widget=forms.CheckboxSelectMultiple,
                        choices=[(c.id, c.choice_text) for c in choices],
                        required=required
                    )
