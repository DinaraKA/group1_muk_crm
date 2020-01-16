from webapp.models import Grade
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class GradeListView(ListView):
    template_name = 'grades/grades.html'
    model = Grade
    ordering = ["value"]
    context_object_name = 'grades'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class GradeCreateView(CreateView):
    model = Grade
    template_name = 'add.html'
    fields = ['value']

    def get_success_url(self):
        return reverse('webapp:grades')


class GradeUpdateView(UpdateView):
    model = Grade
    template_name = 'change.html'
    fields = ['value']

    def get_success_url(self):
        return reverse('webapp:grades')


class GradeDeleteView(DeleteView):
    model = Grade
    template_name = 'delete.html'
    success_url = reverse_lazy('webapp:grades')

