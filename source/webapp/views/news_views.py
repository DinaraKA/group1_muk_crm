from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.models import News


class NewsView(ListView):
    model = News
    template_name = 'news/all_news.html'
    context_object_name = 'news_list'
    ordering = ['-created_at']
    paginate_by = 1
    paginate_orphans = 0


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'


class NewsAddView(CreateView):
    model = News
    template_name = 'add.html'
    fields = ('title', 'text', 'photo')
    success_url = reverse_lazy('webapp:news')

    def get_success_url(self):
        return reverse('webapp:news_detail', kwargs={'pk': self.object.pk})


class NewsEditView(UpdateView):
    template_name = 'change.html'
    model = News
    fields = ('title', 'text', 'photo')
    context_object_name = 'news'

    def get_success_url(self):
        return reverse('webapp:news_detail', kwargs={'pk': self.object.pk})


class NewsDeleteView(DeleteView):
    model = News
    template_name = 'delete.html'
    context_object_name = 'news'
    success_url = reverse_lazy('webapp:news')




