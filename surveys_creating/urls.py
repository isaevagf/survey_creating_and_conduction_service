from django.urls import path, re_path

from . import views

app_name = "surveys_creating"

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
    path('questionnaire_editing/<int:q_id>/',
         views.questionnaire_editing,
         name='questionnaire_editing'),
    path('<int:q_id>/delete/<int:item_id>',
         views.delete_question,
         name='delete_question'),
    path('<int:q_id>/delete/',
         views.delete_questionnaire,
         name='delete_questionnaire'),
]