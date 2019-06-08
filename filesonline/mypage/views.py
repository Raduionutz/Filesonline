import os, shutil

from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import reverse, HttpResponseRedirect, HttpResponse

from file_upload.forms import UploadFileForm
from file_upload.models import File, SharedFileWith

class MainPageView(LoginRequiredMixin, View):

    login_url = 'user/login/'
    redirect_field_name = 'index.html'

    def get(self, request):

        upload_form = UploadFileForm()

        files = os.listdir(request.user.user_profile.folder)

        shared_by_me = request.user.files.filter(shared=True)
        shared_with_me = request.user.shared_with.all()

        context = {
            'files': files,
            'upload_form': upload_form,
            'shared_by_me': shared_by_me,
            'shared_with_me': shared_with_me,
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

                db_file = File()

                db_file.owner = request.user
                db_file.filename = f.name

                db_file.save()

        return HttpResponseRedirect(reverse('mypage:main_page'))

class DeleteFileView(LoginRequiredMixin, View):

    login_url = 'user/login/'
    redirect_field_name = 'index.html'

    def post(self, request):

        file = request.POST.get('file')

        if file:
            db_file = File.objects.filter(owner=request.user, filename=file)

            db_file.delete()

            os.remove(os.path.join(request.user.user_profile.folder, file))

        return HttpResponseRedirect(reverse('mypage:main_page'))


class DownloadFileView(LoginRequiredMixin, View):

    login_url = 'user/login/'
    redirect_field_name = 'index.html'

    def post(self, request):

        file = request.POST.get('file')

        file_path = os.path.join(request.user.user_profile.folder, file)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response

        return HttpResponseRedirect(reverse('mypage:main_page'))


class ShareFileView(LoginRequiredMixin, View):

    login_url = 'user/login/'
    redirect_field_name = 'index.html'

    def post(self, request):

        file = request.POST.get('file')
        share_with = request.POST.get('share_with')

        file_path = os.path.join(request.user.user_profile.folder, file)
        share_with_user = User.objects.get(username=share_with)

        if (
                os.path.exists(file_path)
                and share_with_user
                and share_with_user != request.user
        ):
            shared_file = SharedFileWith()

            existing = SharedFileWith.objects.filter(
                shared_with=share_with_user,
                file__filename=file,
                file__owner=request.user
            )

            if not existing:

                file_to_share = File.objects.get(owner=request.user, filename=file)

                file_to_share.shared = True

                shared_file.file = file_to_share
                shared_file.shared_with = share_with_user

                shared_file.save()
                file_to_share.save()

        return HttpResponseRedirect(reverse('mypage:main_page'))


class MoveSharedFile(LoginRequiredMixin, View):

    login_url = 'user/login/'
    redirect_field_name = 'index.html'

    def post(self, request):

        file = request.POST.get('file')

        print('ceva')

        file_owner = SharedFileWith.objects.get(
                shared_with=request.user,
                file__filename=file
        ).file.owner

        print(file_owner)

        file_path = os.path.join(file_owner.user_profile.folder, file)
        dest_path = os.path.join(request.user.user_profile.folder, file)

        if os.path.exists(file_path):
            shutil.copyfile(file_path, dest_path)
            db_file = File()

            db_file.owner = request.user
            db_file.filename = file

            db_file.save()

        return HttpResponseRedirect(reverse('mypage:main_page'))
