import mock
import pytest
import os

from django.http.request import HttpRequest
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse

from user_login import views, forms, models


def test_register_not_post(monkeypatch):
    render_mock = mock.Mock()
    monkeypatch.setattr(views, 'render', render_mock)

    method = 'get'
    request = HttpRequest()
    request.method = method

    views.register(request=request)

    args, kwargs = render_mock.call_args

    assert args[0] == request
    assert args[1] == 'user_login/register.html'
    assert isinstance(args[2]['user_form'], forms.RegForm)
    assert isinstance(args[2]['user_extra_form'], forms.ExtraRegForm)
    assert not args[2]['registered']

    assert kwargs == {}


@pytest.mark.django_db
def test_register_post_invalid_email(monkeypatch):
    render_mock = mock.Mock()
    monkeypatch.setattr(views, 'render', render_mock)

    mkdir_mock = mock.Mock()
    os.mkdir = mkdir_mock

    method = 'POST'
    request = HttpRequest()
    request.method = method
    request.POST = {
        'username': 'testuser',
        'email': 'invalid email',
        'password': 'passwd',
        'user_picture': None,
        'vault_key': 'test key',
    }

    views.register(request=request)

    args, kwargs = render_mock.call_args

    assert args[0] == request
    assert args[1] == 'user_login/register.html'
    assert isinstance(args[2]['user_form'], forms.RegForm)
    assert isinstance(args[2]['user_extra_form'], forms.ExtraRegForm)
    assert not args[2]['registered']

    assert kwargs == {}


@pytest.mark.django_db
def test_register_post(monkeypatch):
    render_mock = mock.Mock()
    monkeypatch.setattr(views, 'render', render_mock)

    mkdir_mock = mock.Mock()
    os.mkdir = mkdir_mock

    method = 'POST'
    request = HttpRequest()
    request.method = method
    request.POST = {
        'username': 'testuser',
        'email': 'email@mail.com',
        'password': 'passwd',
        'user_picture': None,
        'vault_key': 'test key',
    }

    save_mock_user = mock.Mock()
    save_mock_user_extra = mock.Mock()

    monkeypatch.setattr(User, 'save', value=save_mock_user)
    monkeypatch.setattr(models.UserExtraInfo, 'save', value=save_mock_user_extra)

    result = views.register(request=request)
    assert isinstance(result, HttpResponseRedirect)
    assert result.url == reverse('user_login:login_user')

    assert mkdir_mock.call_count == 2

    assert save_mock_user.call_count == 2
    assert save_mock_user_extra.call_count == 1


@pytest.mark.django_db
def test_login(monkeypatch):
    user = User()
    user.is_active = True

    authenticate_mock = mock.MagicMock(return_value=user)
    login_mock = mock.Mock()

    monkeypatch.setattr(views, 'authenticate', authenticate_mock)
    monkeypatch.setattr(views, 'login', login_mock)

    method = 'POST'
    request = HttpRequest()
    request.method = method

    result = views.login_user(request=request)

    authenticate_mock.assert_called_once()
    login_mock.assert_called_once()

    assert isinstance(result, HttpResponseRedirect)
    assert result.url == reverse('mypage:main_page', kwargs={'path': ''})


@pytest.mark.django_db
def test_login_not_active(monkeypatch):
    user = User()
    user.is_active = False

    authenticate_mock = mock.MagicMock(return_value=user)
    login_mock = mock.Mock()

    monkeypatch.setattr(views, 'authenticate', authenticate_mock)
    monkeypatch.setattr(views, 'login', login_mock)

    method = 'POST'
    request = HttpRequest()
    request.method = method

    result = views.login_user(request=request)

    authenticate_mock.assert_called_once()
    login_mock.assert_not_called()

    assert result.status_code == 200


@pytest.mark.django_db
def test_login_invalid_login(monkeypatch):
    authenticate_mock = mock.MagicMock(return_value=None)
    login_mock = mock.Mock()

    monkeypatch.setattr(views, 'authenticate', authenticate_mock)
    monkeypatch.setattr(views, 'login', login_mock)

    method = 'POST'
    request = HttpRequest()
    request.method = method

    result = views.login_user(request=request)

    authenticate_mock.assert_called_once()
    login_mock.assert_not_called()

    assert result.status_code == 200


@pytest.mark.django_db
def test_login_get(monkeypatch):
    authenticate_mock = mock.MagicMock(return_value=None)
    login_mock = mock.Mock()

    monkeypatch.setattr(views, 'authenticate', authenticate_mock)
    monkeypatch.setattr(views, 'login', login_mock)

    method = 'GET'
    request = HttpRequest()
    request.method = method

    result = views.login_user(request=request)

    authenticate_mock.assert_not_called()
    login_mock.assert_not_called()

    assert result.status_code == 200


def test_logout(monkeypatch):
    logout_mock = mock.Mock()
    monkeypatch.setattr(views, 'logout', logout_mock)

    method = 'GET'
    request = HttpRequest()
    request.method = method

    views.logout(request=request)

    logout_mock.assert_called_once()
