from django.shortcuts import render
from django.views import View


class HomeView(View):
    template_name = 'hortihome/base.html'

    def get(self, request):
        return render(request, self.template_name)
