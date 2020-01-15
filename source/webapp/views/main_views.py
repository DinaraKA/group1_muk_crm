from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from webapp.models import News, Announcements


class IndexView(ListView):
    template_name = 'index.html'
    model = News
    context_object_name = 'news_list'

    def get_queryset(self):
        return News.objects.order_by('-created_at')[0:2]


class IndexView(ListView):
    template_name = 'index.html'
    model = Announcements
    context_object_name = 'announcements'

    def get_queryset(self):
        return Announcements.objects.order_by('-created_at')[0:2]


# class IndexView(TemplateView):
#     template_name = 'list.html'

class Department1View(TemplateView):
    template_name = 'departments/department1.html'

class Department2View(TemplateView):
    template_name = 'departments/department2.html'

class Department3View(TemplateView):
    template_name = 'departments/department3.html'