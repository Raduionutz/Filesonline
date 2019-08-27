import mock
import pytest
import os

from django.http.request import HttpRequest
from django import shortcuts
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

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

    assert isinstance(views.register(request=request), HttpResponseRedirect)
    assert mkdir_mock.call_count == 2

    assert save_mock_user.call_count == 2
    assert save_mock_user_extra.call_count == 1

