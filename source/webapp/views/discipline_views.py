from webapp.forms import DisciplineForm
from webapp.models import Discipline
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class DisciplineListView(ListView):
    template_name = 'disciplines/disciplines.html'
    model = Discipline
    ordering = ["name"]
    context_object_name = 'disciplines'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class DisciplineCreateView(CreateView):
    model = Discipline
    template_name = 'add.html'
    form_class = DisciplineForm

    def get_success_url(self):
        return reverse('webapp:disciplines')


class DisciplineUpdateView(UpdateView):
    model = Discipline
    template_name = 'change.html'
    form_class = DisciplineForm

    def get_success_url(self):
        return reverse('webapp:disciplines')


class DisciplineDeleteView(DeleteView):
    model = Discipline
    template_name = 'delete.html'
    success_url = reverse_lazy('webapp:disciplines')

