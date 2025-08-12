from django.urls import path
from . import views

app_name = "surveys_statistics"

urlpatterns = [
    path("<int:pk>/", views.survey_stats, name="survey_stats"),
]