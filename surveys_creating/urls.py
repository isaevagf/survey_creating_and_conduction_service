from django.urls import path, re_path

from . import views

app_name = "surveys_conducting"

urlpatterns = [
    path("", views.survey_list, name="survey_list"),
    path('<int:q_id>/',
        views.survey_detail,
        name='survey_detail'),
    re_path(r'(?P<q_id>[-\w]+)/question_creating/',
        views.create_question_with_answers,
        name='question_creating'),
    re_path(r'(?P<q_id>[-\w]+)/question_editing/(?P<number>[-\w]+)',
        views.create_question_with_answers,
        name='question_editing'),
    path('questionnaire_creating/',
        views.questionnaire_creating,
        name='questionnaire_creating'),
]