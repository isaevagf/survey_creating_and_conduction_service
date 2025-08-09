from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from surveys_creating.models import Questionnaire, Question, Choice
from .models import Response, Answer
from .forms import SurveyResponseForm


def survey_list(request):
    surveys = Questionnaire.objects.all()
    return render(request, "surveys_conducting/survey_list.html", {"surveys": surveys})


@login_required
def survey_detail(request, survey_id):
    survey = get_object_or_404(Questionnaire, pk=survey_id)

    if Response.objects.filter(questionnaire=survey, user=request.user).exists():
        return HttpResponseForbidden("Вы уже проходили эту анкету.")

    questions = Question.objects.filter(questionnaire=survey, active=True)

    if request.method == "POST":
        form = SurveyResponseForm(request.POST, questions=questions)
        if form.is_valid():
            response = Response.objects.create(questionnaire=survey, user=request.user)

            for question in questions:
                answer_value = form.cleaned_data.get(f"question_{question.id}")

                if isinstance(answer_value, list):
                    for choice_id in answer_value:
                        choice = Choice.objects.get(id=choice_id)
                        Answer.objects.create(response=response, question=question, choice=choice)
                elif answer_value and str(answer_value).isdigit():

                    choice = Choice.objects.get(id=answer_value)
                    Answer.objects.create(response=response, question=question, choice=choice)
                else:
                    Answer.objects.create(response=response, question=question, text_answer=answer_value)

            return redirect("surveys_conducting:survey_complete", survey_id=survey.id)
    else:
        form = SurveyResponseForm(questions=questions)

    return render(request, "surveys_conducting/survey_detail.html", {"survey": survey, "form": form})


def survey_complete(request, survey_id):
    survey = get_object_or_404(Questionnaire, pk=survey_id)
    return render(request, "surveys_conducting/survey_complete.html", {"survey": survey})