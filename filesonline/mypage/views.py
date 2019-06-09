import os, shutil

from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import reverse, HttpResponseRedirect, HttpResponse

from file_upload.forms import UploadFileForm
from file_upload.models import File, SharedFileWith
from filesonline.utils import encrypt_file, decrypt_file


class MainPage(LoginRequiredMixin, View):

    login_url = 'user/login/'
    redirect_field_name = 'index.html'

    def get(self, request, path=''):

        upload_form = UploadFileForm()

        files = File.objects.filter(owner=request.user, path=path).order_by('-is_directory', '-filename')

        shared_by_me = request.user.files.filter(shared=True)
        shared_with_me = request.user.shared_with.all()

        context = {
            'path': path,
            'files': files,
            'upload_form': upload_form,
            'shared_by_me': shared_by_me,
            'shared_with_me': shared_with_me,
        }

        return render(request, 'page/my_page.html', context=context)

    def post(self, request, path):

        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():

            files = request.FILES.getlist('file')

            def handle_uploaded_file(f, filename):
                with open(filename, 'ab+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)

            for f in files:
                print(os.path.join(request.user.user_profile.folder))
                print(path)

                print(os.path.join(os.path.join(request.user.user_profile.folder, path), f.name))
                handle_uploaded_file(
                    request.FILES['file'],
                    os.path.join(os.path.join(request.user.user_profile.folder, path), f.name)
                )

                db_file = File()

                db_file.owner = request.user
                db_file.filename = f.name
                db_file.path = path

                db_file.save()

        return HttpResponseRedirect(reverse('mypage:main_page', kwargs = {'path': path}))


class DeleteFile(LoginRequiredMixin, View):

    login_url = 'user/login/'
    redirect_field_name = 'index.html'

    def post(self, request):

        file = request.POST.get('file')
        path = request.POST.get('path', '')

        if file:
            db_file = File.objects.filter(owner=request.user, filename=file, path=path)

            db_file.delete()

            os.remove(os.path.join(os.path.join(request.user.user_profile.folder, path), file))

        return HttpResponseRedirect(reverse('mypage:main_page', kwargs = {'path': path}))


class DownloadFile(LoginRequiredMixin, View):

    login_url = 'user/login/'
    redirect_field_name = 'index.html'

    def post(self, request):

        file = request.POST.get('file')
        path = request.POST.get('path', '')

        file_path = os.path.join(os.path.join(request.user.user_profile.folder, path), file)


        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response

        return HttpResponseRedirect(reverse('mypage:main_page', kwargs = {'path': path}))


class DecryptDownloadFile(LoginRequiredMixin, View):

    login_url = 'user/login/'
    redirect_field_name = 'index.html'

    def post(self, request):

        file = request.POST.get('file')
        path = request.POST.get('path', '')
        file_path = os.path.join(os.path.join(request.user.user_profile.folder, path), file)

        db_file = File.objects.get(owner=request.user, filename=file, path=path)
        if db_file.encrypted is False:
            return DownloadFile().post(request)

        dec_path = decrypt_file(file_path)

        with open(dec_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(dec_path)

        os.remove(dec_path)

        return response


class ShareFile(LoginRequiredMixin, View):

    login_url = 'user/login/'
    redirect_field_name = 'index.html'

    def post(self, request):

        file = request.POST.get('file')
        path = request.POST.get('path', '')
        share_with = request.POST.get('share_with')

        file_obj = File.objects.get(owner=request.user, filename=file, path=path)

        file_path = os.path.join(os.path.join(request.user.user_profile.folder, file_obj.path), file)
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
                file__owner=request.user,
                file__path=path,
            )

            if not existing:

                file_to_share = File.objects.get(owner=request.user, filename=file, path=path)

                file_to_share.shared = True

                shared_file.file = file_to_share
                shared_file.shared_with = share_with_user

                shared_file.save()
                file_to_share.save()

        return HttpResponseRedirect(reverse('mypage:main_page', kwargs = {'path': path}))


class MoveSharedFile(LoginRequiredMixin, View):

    login_url = 'user/login/'
    redirect_field_name = 'index.html'

    def post(self, request):

        file = request.POST.get('file')
        path = request.POST.get('path', '')

        dest_path = os.path.join(os.path.join(request.user.user_profile.folder, path), file)

        shared_file_obj = SharedFileWith.objects.get(
                shared_with=request.user,
                file__filename=file
        )

        file_owner = shared_file_obj.file.owner
        file_path = os.path.join(
            os.path.join(file_owner.user_profile.folder, shared_file_obj.file.path),
            file,
        )

        if os.path.exists(file_path):
            shutil.copyfile(file_path, dest_path)
            db_file = File()

            db_file.owner = request.user
            db_file.filename = file
            db_file.path = path


            if shared_file_obj.file.encrypted:
                db_file.encrypted = True

            db_file.save()

        return HttpResponseRedirect(reverse('mypage:main_page', kwargs = {'path': path}))


class EncryptFile(LoginRequiredMixin, View):

    login_url = 'user/login/'
    redirect_field_name = 'index.html'

    def post(self, request):

        # path = path[1:]

        file = request.POST.get('file')
        path = request.POST.get('path', '')

        db_file = File.objects.get(owner=request.user, filename=file, path=path)

        if db_file.encrypted is False:
            db_file.filename = db_file.filename + '.enc'
            db_file.encrypted = True

            file_path = os.path.join(os.path.join(request.user.user_profile.folder, path), file)

            encrypt_file(file_path)

            db_file.save()

            os.remove(file_path)

        return HttpResponseRedirect(reverse('mypage:main_page', kwargs = {'path': path}))


class DecryptFile(LoginRequiredMixin, View):

    login_url = 'user/login/'
    redirect_field_name = 'index.html'

    def post(self, request):

        file = request.POST.get('file')
        path = request.POST.get('path', '')

        db_file = File.objects.get(owner=request.user, filename=file, path=path)

        if db_file.encrypted is True:
            db_file.filename = db_file.filename[:-4]
            db_file.encrypted = False

            file_path = os.path.join(os.path.join(request.user.user_profile.folder, path), file)

            decrypt_file(file_path)

            db_file.save()

            os.remove(file_path)

        return HttpResponseRedirect(reverse('mypage:main_page', kwargs = {'path': path}))

class MakeDirectory(LoginRequiredMixin, View):

    login_url = 'user/login/'
    redirect_field_name = 'index.html'

    def post(self, request):

        dir = request.POST.get('dir')
        path = request.POST.get('path', '')

        dir_obj = File.objects.filter(owner=request.user, filename=dir, path=path, is_directory=True)

        if not dir_obj:
            new_dir = File()

            new_dir.owner = request.user
            new_dir.filename = dir
            new_dir.path = path
            new_dir.is_directory = True

            dir_path = os.path.join(os.path.join(request.user.user_profile.folder, path), dir)

            os.mkdir(dir_path)

            new_dir.save()

        return HttpResponseRedirect(reverse('mypage:main_page', kwargs = {'path': path}))


class ChangeDirectory(LoginRequiredMixin, View):

    login_url = 'user/login/'
    redirect_field_name = 'index.html'

    def post(self, request):

        dir = request.POST.get('dir')
        path = request.POST.get('path', '')

        if not dir:
            return HttpResponseRedirect(reverse('mypage:main_page', kwargs={'path': path}))

        dir_obj = File.objects.get(owner=request.user, filename=dir, path=path, is_directory=True)

        if dir_obj:

            path = os.path.join(dir_obj.path, dir)


        return HttpResponseRedirect(reverse('mypage:main_page', kwargs = {'path': path}))


class DeleteDirectory(LoginRequiredMixin, View):

    login_url = 'user/login/'
    redirect_field_name = 'index.html'

    def post(self, request):

        dir = request.POST.get('dir')
        path = request.POST.get('path', '')

        if not dir:
            return HttpResponseRedirect(reverse('mypage:main_page', kwargs={'path': path}))

        dir_obj = File.objects.get(owner=request.user, filename=dir, path=path, is_directory=True)

        if dir_obj:

            shutil.rmtree(os.path.join(os.path.join(request.user.user_profile.folder, path), dir))

            paths_to_delete = [os.path.join(dir_obj.path, dir_obj.filename)]

            user_files = File.objects.filter(owner=request.user)

            while paths_to_delete:

                searched_path = paths_to_delete.pop()

                files = user_files.filter(path=searched_path)

                for file in files:
                    if file.is_directory:
                        paths_to_delete.append(os.path.join(searched_path, file.filename))

                    file.delete()

            dir_obj.delete()

        print(path)


        return HttpResponseRedirect(reverse('mypage:main_page', kwargs = {'path': path}))
