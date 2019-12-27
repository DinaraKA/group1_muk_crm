from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

class Department1View(TemplateView):
    template_name = 'departments/department1.html'

class Department2View(TemplateView):
    template_name = 'departments/department2.html'

class Department3View(TemplateView):
    template_name = 'departments/department3.html'


