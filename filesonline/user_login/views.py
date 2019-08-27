import os, random, string, time

from django.shortcuts import render
from .forms import RegForm, ExtraRegForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'user_login/index.html')


@login_required
def user_logout(request):

    logout(request)

    return HttpResponseRedirect(reverse('user_login:login_user'))


def register(request):

    registered = False

    if request.method == 'POST':

        user_form = RegForm(data=request.POST)
        profile_form = ExtraRegForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)

            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'user_picture' in request.FILES:

                photo = request.FILES['user_picture']

                photo._name = ''.join([
                    user.username,
                    '_',
                    str(int(time.time())),
                    '.jpg',
                ])

                profile.user_picture = photo

            profile.enc_pass = ''.join(
                random.choices(string.ascii_letters + string.digits, k=100),
            )


            profile.folder = os.path.join(os.path.join('media', 'user_files'), str(user.pk))
            os.mkdir(profile.folder)
            os.mkdir(profile.folder + '_vault')

            profile.save()

            registered = True
            return HttpResponseRedirect(reverse('user_login:login_user'))

        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = RegForm()
        profile_form = ExtraRegForm()

    return render(
        request,
        'user_login/register.html',
        {
            'user_form': user_form,
            'user_extra_form': profile_form,
            'registered': registered
        }
    )


def login_user(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('mypage:main_page', kwargs = {'path': ''}))
            else:
                return HttpResponse('Your account is not active.')
        else:
            return HttpResponse('Invalid login details supplied.')

    else:
        return render(request, 'user_login/login.html', {})
