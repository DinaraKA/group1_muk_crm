from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from accounts.models import StudyGroup
from webapp.models import News, Announcements, Discipline


class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'news_list'
    model = News

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'announcements': Announcements.objects.order_by('-created_at')[0:2],
            'groups': StudyGroup.objects.all().order_by('name'),
            'disciplines': Discipline.objects.all()
        })
        return context

    def get_queryset(self):
        return News.objects.order_by('-created_at')[0:2]


class Department1View(TemplateView):
    template_name = 'departments/department1.html'

class Department2View(TemplateView):
    template_name = 'departments/department2.html'

class Department3View(TemplateView):
    template_name = 'departments/department3.html'