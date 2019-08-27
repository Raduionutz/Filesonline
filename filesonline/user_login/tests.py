import mock

from django.http.request import HttpRequest
from django import shortcuts

from user_login import views
from user_login import forms


def test_register():
    origRender = shortcuts.render
    renderMock = mock.Mock()

    setattr(views, 'render', renderMock)

    method = 'get'
    request = HttpRequest()
    request.method = method

    views.register(request=request)

    args, kwargs = renderMock.call_args

    assert args[0] == request
    assert args[1] == 'user_login/register.html'
    assert isinstance(args[2]['user_form'], forms.RegForm)
    assert isinstance(args[2]['user_extra_form'], forms.ExtraRegForm)
    assert not args[2]['registered']

    assert kwargs == {}


