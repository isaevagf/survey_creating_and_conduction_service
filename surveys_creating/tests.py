import pytest
from django.urls import reverse
from surveys_creating.models import Questionnaire, Question, Choice
from surveys_creating.forms import ChoiceForm, QuestionForm, QuestionnaireForm


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username="test", password="pass")


@pytest.fixture
def questionnaire(db, user):
    return Questionnaire.objects.create(
        q_id=1,
        name="Test Q",
        max_questions=5,
        author=user
    )


@pytest.fixture
def auth_client(client, user):
    client.login(username="test", password="pass")
    return client


@pytest.mark.django_db
def test_choice_form_valid():
    form = ChoiceForm(data={"choice_text": "Option 1", "choice_points": 1})
    assert form.is_valid()


@pytest.mark.django_db
def test_choice_form_invalid():
    form = ChoiceForm(data={})
    assert not form.is_valid()


@pytest.mark.django_db
def test_question_form_valid():
    form = QuestionForm(data={"question_text": "What?", "active": True})
    assert form.is_valid()


@pytest.mark.django_db
def test_questionnaire_form_valid():
    form = QuestionnaireForm(data={"name": "Survey", "max_questions": 3})
    assert form.is_valid()


def test_create_question_redirect_if_not_logged_in(client, questionnaire):
    url = reverse("surveys_creating:question_creating", args=[questionnaire.q_id])
    response = client.get(url)
    assert response.status_code == 302


def test_create_question_ok_if_logged_in(auth_client, questionnaire):
    url = reverse("surveys_creating:question_creating", args=[questionnaire.q_id])
    response = auth_client.get(url)
    assert response.status_code == 200


def test_create_question_post_creates_data(auth_client, questionnaire):
    url = reverse("surveys_creating:question_creating", args=[questionnaire.q_id])

    post_data = {
        "question_text": "New Question",
        "active": True,
        "choice_set-INITIAL_FORMS": "0",
        "choice_set-TOTAL_FORMS": "4",
        "choice_set-MIN_NUM_FORMS": "0",
        "choice_set-MAX_NUM_FORMS": str(questionnaire.max_questions),
        "choice_set-0-choice_text": "Choice 1",
        "choice_set-0-choice_points": 1,
        "choice_set-1-choice_text": "Choice 2",
        "choice_set-1-choice_points": 2,
        "choice_set-2-choice_text": "Choice 3",
        "choice_set-2-choice_points": 3,
        "choice_set-3-choice_text": "Choice 4",
        "choice_set-3-choice_points": 4,
    }
    response = auth_client.post(url, post_data, follow=True)
    assert response.status_code == 200
    assert Question.objects.count() == 1
    assert Choice.objects.count() == 4
