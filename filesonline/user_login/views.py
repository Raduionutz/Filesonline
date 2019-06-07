import os, time

from django.shortcuts import render
from .forms import RegForm, ExtraRegForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request,'user_login/index.html')


@login_required
def user_logout(request):

    logout(request)

    return HttpResponseRedirect(reverse('user_login:login_user'))


def register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        user_form = RegForm(data=request.POST)
        profile_form = ExtraRegForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'user_picture' in request.FILES:

                photo = request.FILES['user_picture']

                photo._name = ''.join([
                    user.username,
                    '_',
                    str(int(time.time())),
                    '.jpg',
                ])

                profile.user_picture = photo

            profile.save()

            os.mkdir(os.path.join(os.path.join('media', 'user_files'), str(user.pk)))

            registered = True

        else:
            # One of the forms was invalid if this gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = RegForm()
        profile_form = ExtraRegForm()

    return render(
        request,
        'user_login/register.html',
        {
            'user_form':user_form,
            'user_extra_form':profile_form,
            'registered':registered
        }
    )


def login_user(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('user_login:index'))
            else:
                # If account is not active:
                return HttpResponse('Your account is not active.')
        else:
            return HttpResponse('Invalid login details supplied.')

    else:
        #Nothing has been provided for username or password.
        return render(request, 'user_login/login.html', {})
