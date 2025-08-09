from django.db import models
from django.conf import settings

from surveys_creating.models import Questionnaire


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    date_of_birth = models.DateField(blank=True, null=True)
    questionnaires = models.ManyToManyField(Questionnaire, blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)