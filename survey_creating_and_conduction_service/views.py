from django.shortcuts import render

from surveys_creating.models import Questionnaire

def index(request):
    my_surveys = []
    has_surveys = False
    if request.user.is_authenticated:
        my_surveys = Questionnaire.objects.filter(author=request.user)
        has_surveys = my_surveys.exists()

    return render(request, "index.html", {
        "has_surveys": has_surveys,
        "my_surveys": my_surveys
    })