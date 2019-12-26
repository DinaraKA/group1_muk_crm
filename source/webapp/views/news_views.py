from django.views.generic import ListView, DetailView
from webapp.models import News


class NewsView(ListView):
    model = News
    template_name = 'news/all_news.html'
    context_object_name = 'news_list'
    ordering = ['-created_at']


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/detail.html'
    context_object_name = 'news'
