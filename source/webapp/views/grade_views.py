from django.contrib.auth.mixins import UserPassesTestMixin

from webapp.models import Grade
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class GradeListView(UserPassesTestMixin, ListView):
    template_name = 'grades/grades.html'
    model = Grade
    ordering = ["value"]
    context_object_name = 'grades'

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class GradeCreateView(UserPassesTestMixin, CreateView):
    model = Grade
    template_name = 'add.html'
    fields = ['value', 'description']

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

    def get_success_url(self):
        return reverse('webapp:grades')


class GradeUpdateView(UserPassesTestMixin, UpdateView):
    model = Grade
    template_name = 'change.html'
    fields = ['value', 'description']

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

    def get_success_url(self):
        return reverse('webapp:grades')


class GradeDeleteView(UserPassesTestMixin, DeleteView):
    model = Grade
    template_name = 'delete.html'
    success_url = reverse_lazy('webapp:grades')

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

