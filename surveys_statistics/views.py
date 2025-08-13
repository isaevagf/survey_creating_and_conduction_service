from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from surveys_creating.models import Questionnaire, Question, Choice
from surveys_conducting.models import Response, Answer


@login_required
def survey_stats(request, pk):
    questionnaire = get_object_or_404(Questionnaire, pk=pk)

    if request.user != questionnaire.author:
        return render(request, "403.html", status=403)

    total_responses = Response.objects.filter(questionnaire=questionnaire).count()
    unique_users = Response.objects.filter(questionnaire=questionnaire).values("user").distinct().count()

    questions_stats = []
    for question in Question.objects.filter(questionnaire=questionnaire):
        multi_choices = Choice.objects.filter(question=question)
        answers = Answer.objects.filter(response__questionnaire=questionnaire, question=question)
        total_answers = answers.count()

        if multi_choices.exists():
            choice_counts = []
            for choice in Choice.objects.filter(question=question):
                count = answers.filter(choice=choice).count()
                total_points = sum(a.choice.choice_points for a in answers.filter(choice=choice))
                percent = round((count / total_answers) * 100, 2) if total_answers > 0 else 0

                choice_counts.append({
                    "text": choice.choice_text,
                    "count": count,
                    "points": total_points,
                    "percent": percent
                })

            questions_stats.append({
                "question": question.question_text,
                "choices": choice_counts
            })
        else:
            text_answers = answers.values_list("text_answer", flat=True)
            questions_stats.append({
                "question": question.question_text,
                "choices": [],
                "text_answers": list(text_answers)
            })

    context = {
        "questionnaire": questionnaire,
        "total_responses": total_responses,
        "unique_users": unique_users,
        "questions_stats": questions_stats
    }
    return render(request, "surveys_statistics/survey_stats.html", context)
