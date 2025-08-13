from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from surveys_creating.models import Questionnaire, Question, Choice
from .models import Response, Answer
from .forms import SurveyResponseForm

def survey_list(request):
    surveys = Questionnaire.objects.all()
    return render(request, "surveys_conducting/survey_list.html", {"surveys": surveys})


from django.shortcuts import render, get_object_or_404, redirect
from surveys_creating.models import Questionnaire, Question, Choice
from .forms import SurveyResponseForm
from .models import Response, Answer
from django.contrib.auth.decorators import login_required


@login_required
def survey_detail(request, survey_id):
    questionnaire = get_object_or_404(Questionnaire, pk=survey_id)
    questions = Question.objects.filter(questionnaire=questionnaire, active=True)

    existing_response = Response.objects.filter(
        questionnaire=questionnaire,
        user=request.user
    ).order_by("-created_at").first()

    if existing_response and "retry" not in request.GET:
        return render(request, "surveys_conducting/survey_retry_confirm.html", {
            "questionnaire": questionnaire
        })

    if request.method == "POST":
        form = SurveyResponseForm(request.POST, questions=questions)
        if form.is_valid():
            response = Response.objects.create(
                questionnaire=questionnaire,
                user=request.user
            )
            for question in questions:
                field_name = f"question_{question.pk}"
                answer_value = form.cleaned_data[field_name]

                if isinstance(answer_value, list):
                    for choice_id in answer_value:
                        choice = Choice.objects.get(pk=choice_id)
                        Answer.objects.create(
                            response=response,
                            question=question,
                            choice=choice
                        )
                # else:
                #     try:
                #         choice_id = int(answer_value)
                #         choice = Choice.objects.get(pk=choice_id)
                #         Answer.objects.create(
                #             response=response,
                #             question=question,
                #             choice=choice
                #         )
                #     except (ValueError, Choice.DoesNotExist):
                #         Answer.objects.create(
                #             response=response,
                #             question=question,
                #             text_answer=answer_value
                #         )

                elif str(answer_value).isdigit():
                    choice = Choice.objects.get(pk=int(answer_value))
                    Answer.objects.create(
                        response=response,
                        question=question,
                        choice=choice
                    )

                elif answer_value:
                    Answer.objects.create(
                        response=response,
                        question=question,
                        text_answer=answer_value
                    )

            return redirect("surveys_conducting:survey_complete", survey_id=survey_id)
    else:
        form = SurveyResponseForm(questions=questions)

    return render(request, "surveys_conducting/survey_detail.html", {
        "questionnaire": questionnaire,
        "form": form
    })



def survey_complete(request, survey_id):
    survey = get_object_or_404(Questionnaire, pk=survey_id)
    return render(request, "surveys_conducting/survey_complete.html", {"survey": survey})

@login_required
def available_surveys(request):
    surveys = Questionnaire.objects.all()
    return render(request, 'surveys_conducting/survey_list.html', {'surveys': surveys})