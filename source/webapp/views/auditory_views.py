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