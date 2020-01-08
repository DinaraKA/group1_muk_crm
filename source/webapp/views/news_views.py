from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView
from webapp.models import News


class NewsView(ListView):
    model = News
    template_name = 'news/all_news.html'
    context_object_name = 'news_list'
    ordering = ['-created_at']
    paginate_by = 2
    paginate_orphans = 0


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/detail.html'
    context_object_name = 'news'


class NewsAddView(LoginRequiredMixin, CreateView):
    model = News
    template_name = 'news/add.html'
    fields = ('title', 'text', 'photo')
    success_url = reverse_lazy('webapp:news')
    permission_required = 'webapp.add_news'
    permission_denied_message = "Доступ запрещен"


    def get_success_url(self):
        return reverse('webapp:new_detail', kwargs={'pk': self.object.pk})


