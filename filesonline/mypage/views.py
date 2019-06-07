import os

from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse, HttpResponseRedirect

from file_upload.forms import UploadFileForm

class MainPageView(LoginRequiredMixin, View):

    login_url = 'user/login/'
    redirect_field_name = 'index.html'

    def get(self, request):

        upload_form = UploadFileForm()

        files = os.listdir(request.user.user_profile.folder)

        context = {
            'files': files,
            'upload_form': upload_form,
        }

        return render(request, 'page/my_page.html', context=context)

    def post(self, request):

        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():

            files = request.FILES.getlist('file')

            def handle_uploaded_file(f, filename):
                with open(filename, 'ab+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)

            for f in files:
                handle_uploaded_file(
                    request.FILES['file'],
                    os.path.join(request.user.user_profile.folder, f.name)
                )

        return HttpResponseRedirect(reverse('mypage:main_page'))

class DeleteFileView(LoginRequiredMixin, View):

    login_url = 'user/login/'
    redirect_field_name = 'index.html'

    def post(self, request):

        file = request.POST.get('file')

        if file:
            os.remove(os.path.join(request.user.user_profile.folder, file))

        return HttpResponseRedirect(reverse('mypage:main_page'))
