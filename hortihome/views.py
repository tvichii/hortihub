from django.shortcuts import render
from django.views import generic, View

# Create your views here.

class HomeView(View):
    template_name = 'hortihome/base.html'

    def get(self, request):
        return render(request, self.template_name)
