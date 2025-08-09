from django.shortcuts import get_object_or_404, render

from surveys_creating.forms import QuestionForm
from surveys_creating.models import Questionnaire


def questionnaire_detail(request, questionnaire, name):
    post = get_object_or_404(Questionnaire, name=name)
    # List of active questions for this questionnaire
    questions = questionnaire.questions.filter(active=True)

    if request.method == 'POST':
        # A comment was posted
        question_form = QuestionForm(data=request.POST)
        if question_form.is_valid():
            # Create question object but don't save to database yet
            new_question = question_form.save(commit=False)
            # Assign the current questionnaire to the question
            new_question.questionnaire = questionnaire
            # Save the question to the database
            new_question.save()
    else:
        question_form = QuestionForm()
    return render(request,
                  'questionnaire/detail.html',
                 {'questionnaire': questionnaire,
                  'questions': questions,
                  'question_form': question_form})