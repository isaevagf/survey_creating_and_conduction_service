"""
URL configuration for survey_creating_and_conduction_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path

from survey_creating_and_conduction_service.views import index

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('user/', include("authorization.urls")),
    path('surveys_conducting/', include('surveys_conducting.urls', namespace='surveys_conducting')),
    path("surveys_creating/", include("surveys_creating.urls", namespace='surveys_creating')),
    path("surveys_statistics/", include("surveys_statistics.urls", namespace="surveys_statistics")),
]


def custom_page_not_found(request, exception):
    return render(request, "404.html", status=404)

handler404 = "survey_creating_and_conduction_service.urls.custom_page_not_found"
