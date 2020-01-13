from webapp.models import Auditory
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class AuditoryListView(ListView):
    template_name = 'auditory/auditories.html'
    model = Auditory
    ordering = ["-name"]
    context_object_name = 'auditories'
    paginate_by = 20
    paginate_orphans = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class AuditoryCreateView(CreateView):
    model = Auditory
    template_name = 'add.html'
    fields = ['name', 'places', 'description']

    def get_success_url(self):
        return reverse('webapp:auditories')


class AuditoryUpdateView(UpdateView):
    model = Auditory
    template_name = 'change.html'
    fields = ['name', 'places', 'description']

    def get_success_url(self):
        return reverse('webapp:auditories')

