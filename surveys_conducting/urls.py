from django.urls import path
from . import views

app_name = "surveys_conducting"

urlpatterns = [
    path("", views.survey_list, name="survey_list"),
    path("<int:survey_id>/", views.survey_detail, name="survey_detail"),
    path("<int:survey_id>/complete/", views.survey_complete, name="survey_complete"),
]