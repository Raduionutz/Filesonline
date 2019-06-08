from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from django.views.generic.edit import FormView

# Create your views here.


def upload_index(request):
    return render(request, 'upload_test/index.html')


def upload_file(request, path):

    print(path)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            files = request.FILES.getlist('file')

            def handle_uploaded_file(f, filename):
                with open(filename, 'ab+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)

            for f in files:
                handle_uploaded_file(request.FILES['file'], f.name)

            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload_test/form.html', {'form': form})
