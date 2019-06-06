from django.shortcuts import render
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin

class MainPageView(LoginRequiredMixin, View):

    login_url = 'user/login/'
    redirect_field_name = 'index.html'

    def get(self, request):
        return render(request, 'page/my_page.html')
