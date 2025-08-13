from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect

from surveys_creating.forms import QuestionForm, ChoiceForm, QuestionnaireForm
from surveys_creating.models import Questionnaire, Question, Choice

@login_required
def create_question_with_answers(request, q_id, number=None):
    questionnaire = get_object_or_404(Questionnaire, q_id=q_id)
    ChoiceFormSet = inlineformset_factory(Question, Choice, form=ChoiceForm, can_delete=False,
                                          extra=4, max_num=questionnaire.max_questions)
    if number:
        question = Question.objects.get(number=number)
    else:
        question = Question(questionnaire_id=q_id)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST, request.FILES, instance=question)
        choice_formset = ChoiceFormSet(request.POST, instance=question)
        if question_form.is_valid():
            new_question = question_form.save()

            if question.pk:
                qq = question
            else:
                qq = Question.objects.filter(questionnaire_id=q_id, question_text=new_question.question_text).last()

            if choice_formset.is_valid():
                choice_formset.instance = qq
                choice_formset.save()

            return redirect('surveys_creating:survey_detail', q_id=q_id)

    else:
        question_form = QuestionForm(instance=question)
        choice_formset = ChoiceFormSet(instance=question)

    return render(request, 'surveys_creating/question_creating.html',
                  {'question_form': question_form, 'choice_formset': choice_formset})


def survey_detail(request, q_id):
    questionnaire = get_object_or_404(Questionnaire, pk=q_id)
    questions = Question.objects.filter(questionnaire=questionnaire).order_by('-number')
    choices = Choice.objects.filter(question__in = questions)
    questionnaire_form = QuestionnaireForm(instance=questionnaire)

    return render(request, 'surveys_creating/survey_detail.html',
                  {'questionnaire': questionnaire,
                   'questions': questions,
                   'choices': choices,
                   'questionnaire_form': questionnaire_form})


@login_required
def survey_list(request):
    surveys = Questionnaire.objects.filter(author=request.user)
    return render(request, "surveys_creating/survey_list.html", {"surveys": surveys})

@login_required
def questionnaire_creating(request):
    questionnaire_form = QuestionnaireForm(request.POST)
    if questionnaire_form.is_valid():
        instance = questionnaire_form.save(commit=False)
        instance.author = request.user
        instance.save()
        qq = Questionnaire.objects.filter(author=request.user, name = instance.name).last()
        return redirect('surveys_creating:survey_detail', q_id=qq.q_id)
    else:
        questionnaire_form = QuestionnaireForm()

    return render(request, 'surveys_creating/survey_form.html', {'form': questionnaire_form})

@login_required
def questionnaire_editing(request, q_id):
    questionnaire = get_object_or_404(Questionnaire, pk=q_id)

    if request.method == 'POST':
        questionnaire_form = QuestionnaireForm(request.POST, instance=questionnaire)
        if questionnaire_form.is_valid():
            questionnaire_form.save()
            return redirect('surveys_creating:survey_detail', q_id=q_id)
    else:
        questionnaire_form = QuestionnaireForm(instance=questionnaire)
    return render(request, 'surveys_creating/survey_form.html',
                  {'form': questionnaire_form})

def delete_question(request, q_id, item_id):
    question = get_object_or_404(Question, pk=item_id)
    if question:
        question.delete()
    return redirect('surveys_creating:survey_detail', q_id=q_id)

def delete_questionnaire(request, q_id):
    questionnaire = get_object_or_404(Questionnaire, pk=q_id)
    if questionnaire:
        questionnaire.delete()
    return redirect('surveys_creating:survey_list')