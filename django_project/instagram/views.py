from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


class MainView(View):
    template_name = 'instagram/index.html'

    def get(self, request):
        return render(request, self.template_name)
