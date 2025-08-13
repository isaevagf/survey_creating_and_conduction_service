import pytest
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_registration_success(client):
    url = reverse("authorization:register")
    data = {
        "username": "newuser",
        "first_name": "John",
        "email": "john@example.com",
        "password": "pass1234",
        "password2": "pass1234"
    }
    response = client.post(url, data)
    assert response.status_code in (200, 302)
    assert User.objects.filter(username="newuser").exists()


@pytest.mark.django_db
def test_registration_password_mismatch(client):
    url = reverse("authorization:register")
    data = {
        "username": "user2",
        "first_name": "Jane",
        "email": "jane@example.com",
        "password": "pass1234",
        "password2": "wrongpass"
    }
    response = client.post(url, data)
    assert b"Passwords don&#x27;t match" in response.content
    assert not User.objects.filter(username="user2").exists()


@pytest.mark.django_db
def test_login_success(client):
    user = User.objects.create_user(username="loginuser", password="pass1234")
    url = reverse("authorization:login")
    response = client.post(url, {"username": "loginuser", "password": "pass1234"})
    assert response.status_code in (200, 302)
    assert "_auth_user_id" in client.session


@pytest.mark.django_db
def test_login_fail(client):
    url = reverse("authorization:login")
    response = client.post(url, {"username": "nouser", "password": "wrong"})
    assert b"Please enter a correct" in response.content or response.status_code == 200



@pytest.mark.django_db
def test_dashboard_requires_login(client):
    url = reverse("authorization:dashboard")
    response = client.get(url)
    assert response.status_code == 302
    assert reverse("authorization:login") in response.url


@pytest.mark.django_db
def test_dashboard_access_after_login(client):
    User.objects.create_user(username="dashuser", password="pass1234")
    client.login(username="dashuser", password="pass1234")
    url = reverse("authorization:dashboard")
    response = client.get(url)
    assert response.status_code == 200
    assert "личный кабинет" in response.content.decode().lower()