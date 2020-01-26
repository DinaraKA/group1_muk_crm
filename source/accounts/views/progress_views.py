from accounts.models import Progress
from django.urls import reverse, reverse_lazy
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class ProgressIndexView(ListView):
    template_name = 'progress/list.html'
    model = Progress
    context_object_name = 'progress'
    paginate_by = 30
    paginate_orphans = 0
    page_kwarg = 'page'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class ProgressCreateView(CreateView):
    model = Progress
    template_name = 'add.html'
    fields = ['student', 'date', 'discipline', 'theme', 'grade']

    def get_success_url(self):
        return reverse('accounts:progress')

class ProgressUpdateView(UpdateView):
    model = Progress
    template_name = 'change.html'
    fields = ['grade']

    def get_success_url(self):
        return reverse('accounts:progress')

class ProgressDeleteView(DeleteView):
    model = Progress
    template_name = 'delete.html'
    success_url = reverse_lazy('accounts:progress')


