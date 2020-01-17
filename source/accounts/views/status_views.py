from accounts.models import Status
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class StatusListView(ListView):
    template_name = 'status/statuses.html'
    model = Status
    ordering = ["-name"]
    context_object_name = 'statuses'
    paginate_by = 20
    paginate_orphans = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class StatusCreateView(CreateView):
    model = Status
    template_name = 'add.html'
    fields = ['name']

    def get_success_url(self):
        return reverse('accounts:statuses')


class StatusUpdateView(UpdateView):
    model = Status
    template_name = 'change.html'
    fields = ['name']

    def get_success_url(self):
        return reverse('accounts:statuses')


class StatusDeleteView(DeleteView):
    model = Status
    template_name = 'delete.html'
    success_url = reverse_lazy('accounts:statuses')