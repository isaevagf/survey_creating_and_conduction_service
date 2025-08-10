from django.urls import path, re_path

from . import views

app_name = "surveys_conducting"

urlpatterns = [
    path("", views.survey_list, name="survey_list"),
    re_path(r'(?P<q_id>[-\w]+)/$',
        views.survey_detail,
        name='survey_detail'),
    re_path(r'(?P<q_id>[-\w]+)/$',
        views.manage_parent,
        name='question_creating'),
]