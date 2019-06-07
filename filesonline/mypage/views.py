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

        context = {
            'upload_form': upload_form,
        }

        return render(request, 'page/my_page.html', context=context)

    def post(self, request):

        print(request.__dict__.keys())

        print(request.user)
        print(request.FILES)
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():

            files = request.FILES.getlist('file')

            user_folder = os.path.join(os.path.join('media', 'user_files'), str(request.user.pk))

            def handle_uploaded_file(f, filename):
                with open(filename, 'ab+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)

            for f in files:
                handle_uploaded_file(
                    request.FILES['file'],
                    os.path.join(user_folder, f.name)
                )

        return HttpResponseRedirect(reverse('mypage:main_page'))
