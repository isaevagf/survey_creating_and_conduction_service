from django.urls import path, re_path

from . import views

app_name = "surveys_creating"

urlpatterns = [
    path("", views.survey_list, name="survey_list"),
    re_path(r'(?P<q_id>[-\w]+)/$',
        views.survey_detail,
        name='survey_detail'),
    re_path(r'(?P<q_id>[-\w]+)/question_creating/',
        views.create_question_with_answers,
        name='question_creating'),
    re_path(r'(?P<q_id>[-\w]+)/question_editing/(?P<number>[-\w]+)',
        views.create_question_with_answers,
        name='question_editing'),
]