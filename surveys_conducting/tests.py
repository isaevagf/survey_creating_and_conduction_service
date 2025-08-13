import pytest
from django.contrib.auth import get_user_model

from surveys_conducting.forms import SurveyResponseForm
from surveys_creating.models import Questionnaire, Question, Choice

@pytest.fixture
def user(db):
    return get_user_model().objects.create_user(
        username="test",
        password="pass"
    )

@pytest.fixture
def questionnaire(db, user):
    return Questionnaire.objects.create(
        q_id=1,
        name="Test survey",
        author=user,
        max_questions=5
    )

@pytest.fixture
def text_question(db, questionnaire):
    return Question.objects.create(
        questionnaire=questionnaire,
        number=1,
        question_text="Text question?",
        active=True
    )

@pytest.fixture
def single_choice_question(db, questionnaire):
    q = Question.objects.create(
        questionnaire=questionnaire,
        number=2,
        question_text="Single choice?",
        active=True
    )
    Choice.objects.create(
        question=q,
        number=1,
        choice_text="Option 1",
        choice_points=1
    )
    return q


@pytest.fixture
def multi_choice_question(db, questionnaire):
    q = Question.objects.create(
        questionnaire=questionnaire,
        number=3,
        question_text="Multiple choice?",
        active=True
    )
    Choice.objects.create(
        question=q,
        number=10,
        choice_text="Option A",
        choice_points=1
    )
    Choice.objects.create(
        question=q,
        number=11,
        choice_text="Option B",
        choice_points=2
    )
    return q

@pytest.mark.django_db
def test_form_creates_text_field(text_question):
    assert text_question.pk is not None, f"Question is not saved: {text_question}"
    assert Question.objects.filter(pk=text_question.pk).exists()
    form = SurveyResponseForm(questions=[text_question])
    assert f"question_{text_question.pk}" in form.fields
    assert form.fields[f"question_{text_question.pk}"].__class__.__name__ == "CharField"


@pytest.mark.django_db
def test_form_creates_single_choice_field(single_choice_question):
    form = SurveyResponseForm(questions=[single_choice_question])
    field = form.fields[f"question_{single_choice_question.pk}"]
    assert field.__class__.__name__ == "ChoiceField"
    assert len(field.choices) == 1


@pytest.mark.django_db
def test_form_creates_multi_choice_field(multi_choice_question):
    form = SurveyResponseForm(questions=[multi_choice_question])
    field = form.fields[f"question_{multi_choice_question.pk}"]
    assert field.__class__.__name__ == "ChoiceField"
    assert len(field.choices) == 2
