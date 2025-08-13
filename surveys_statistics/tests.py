import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from surveys_creating.models import Questionnaire, Question, Choice
from surveys_conducting.models import Response, Answer

User = get_user_model()

@pytest.fixture
def author(db):
    return User.objects.create_user(username="author", password="pass")

@pytest.fixture
def other_user(db):
    return User.objects.create_user(username="other", password="pass")

@pytest.fixture
def questionnaire(db, author):
    return Questionnaire.objects.create(
        q_id=1,
        name="Stats survey",
        author=author,
        max_questions=5
    )

@pytest.fixture
def text_question(db, questionnaire):
    return Question.objects.create(
        questionnaire=questionnaire,
        number=1,
        question_text="Text Q?",
        active=True
    )

@pytest.fixture
def choice_question(db, questionnaire):
    q = Question.objects.create(
        questionnaire=questionnaire,
        number=2,
        question_text="Choice Q?",
        active=True
    )
    Choice.objects.create(
        question=q, number=10, choice_text="Opt A", choice_points=1
    )
    Choice.objects.create(
        question=q, number=11, choice_text="Opt B", choice_points=2
    )
    return q

@pytest.mark.django_db
def test_stats_text_answers(client, author, questionnaire, text_question):
    resp = Response.objects.create(
        questionnaire=questionnaire, user=author
    )
    Answer.objects.create(response=resp, question=text_question, text_answer="My answer")

    client.login(username="author", password="pass")
    url = reverse("surveys_statistics:survey_stats", args=[questionnaire.pk])
    response = client.get(url)

    assert response.status_code == 200
    ctx = response.context
    assert ctx["total_responses"] == 1
    assert ctx["unique_users"] == 1
    assert ctx["questions_stats"][0]["text_answers"] == ["My answer"]


@pytest.mark.django_db
def test_stats_choice_answers(client, author, questionnaire, choice_question):
    choice_a = choice_question.choice_set.get(choice_text="Opt A")
    choice_b = choice_question.choice_set.get(choice_text="Opt B")

    resp1 = Response.objects.create(questionnaire=questionnaire, user=author)
    Answer.objects.create(response=resp1, question=choice_question, choice=choice_a)

    resp2 = Response.objects.create(questionnaire=questionnaire, user=author)
    Answer.objects.create(response=resp2, question=choice_question, choice=choice_b)

    client.login(username="author", password="pass")
    url = reverse("surveys_statistics:survey_stats", args=[questionnaire.pk])
    response = client.get(url)

    assert response.status_code == 200
    ctx = response.context
    stats = ctx["questions_stats"][0]["choices"]
    assert any(c["text"] == "Opt A" and c["count"] == 1 for c in stats)
    assert any(c["text"] == "Opt B" and c["points"] == 2 for c in stats)
    assert sum(c["percent"] for c in stats) == 100


@pytest.mark.django_db
def test_stats_access_denied_for_non_author(client, other_user, questionnaire):
    client.login(username="other", password="pass")
    url = reverse("surveys_statistics:survey_stats", args=[questionnaire.pk])
    response = client.get(url)
    assert response.status_code == 403