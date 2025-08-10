from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect

from surveys_creating.forms import QuestionForm, ChoiceForm
from surveys_creating.models import Questionnaire, Question, Choice

def create_question_with_answers(request, q_id, number=None):
    question = None
    forms = 0
    if number:
        question = Question.objects.get(pk=number)
        forms = Choice.objects.filter(question=question).count()

    ChoiceFormSet = inlineformset_factory(Question, Choice, form=ChoiceForm, extra=4-forms)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, instance=question)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.questionnaire_id = q_id
            question.save()
            choice_formset = ChoiceFormSet(request.POST, instance=question)
            if choice_formset.is_valid():
                choice_formset.instance = question
                choice_formset.save()
                for form in choice_formset:
                    # Access validated data for each form
                    if form.is_valid() and form.cleaned_data.get("choice_text"):
                        choice = form.save(commit=False)
                        choice.choice_text = form.cleaned_data.get("choice_text")
                        choice.choice_points = form.cleaned_data.get("choice_points")
                        choice.question = question
                        choice.save()

                return redirect('surveys_creating:survey_detail', q_id=q_id)
        else:
            choice_formset = ChoiceFormSet(instance=question)
    else:
        question_form = QuestionForm(instance=question)
        choice_formset = ChoiceFormSet(instance=question)

    return render(request, 'surveys_creating/question_creating.html',
                  {'question_form': question_form, 'choice_formset': choice_formset})


def survey_detail(request, q_id):
    questionnaire = get_object_or_404(Questionnaire, pk=q_id)
    questions = Question.objects.filter(questionnaire=questionnaire)
    choices = Choice.objects.filter(question__in = questions)

    return render(request, 'surveys_creating/survey_detail.html',
                  {'questionnaire': questionnaire,
                   'questions': questions,
                   'choices': choices})


@login_required
def survey_list(request):
    surveys = Questionnaire.objects.filter(author=request.user)
    return render(request, "surveys_creating/survey_list.html", {"surveys": surveys})
