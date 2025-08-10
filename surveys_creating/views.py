from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect

from surveys_creating.forms import QuestionForm, ChoiceForm
from surveys_creating.models import Questionnaire, Question, Choice

ChoiceFormSet = inlineformset_factory(Question, Choice, fields=('choice_text', 'choice_points'))

def manage_parent(request, parent_id=None):
    if parent_id:
        parent = Question.objects.get(pk=parent_id)
    else:
        parent = Question()
    if request.method == 'POST':
        parent_form = QuestionForm(request.POST, instance=parent)
        child_formset = ChoiceFormSet(request.POST, instance=parent)
        if parent_form.is_valid() and child_formset.is_valid():
            parent_instance = parent_form.save()
            child_formset.instance = parent_instance
            child_formset.save()
            return redirect('surveys_creating:survey_list')
    else:
        parent_form = QuestionForm(instance=parent)
        child_formset = ChoiceFormSet(instance=parent)

    return render(request, 'surveys_creating/question_creating.html', {'parent_form': parent_form, 'child_formset': child_formset})

def survey_detail(request, q_id):
    questionnaire = get_object_or_404(Questionnaire, pk=q_id)
    questions = Question.objects.filter(questionnaire=questionnaire)

    if request.method == 'POST':
        # A question was posted
        question_form = QuestionForm(data=request.POST)
        choice_form_1 = ChoiceForm(data=request.POST)
        if question_form.is_valid():
            # Create question object but don't save to database yet
            new_question = question_form.save(commit=False)
            new_choice_1 = choice_form_1.save(commit=False)
            # Assign the current questionnaire to the question
            new_question.questionnaire = questionnaire
            # Save the question to the database
            new_question.save()
    else:
        question_form = QuestionForm()
        choice_form_1 = ChoiceForm()

    return render(request, 'surveys_creating/survey_detail.html',
                  {'questionnaire': questionnaire,
                   'questions': questions,
                   'question_form': question_form,
                   'choice_form_1':choice_form_1})


@login_required
def survey_list(request):
    surveys = Questionnaire.objects.filter(author=request.user)
    return render(request, "surveys_creating/survey_list.html", {"surveys": surveys})