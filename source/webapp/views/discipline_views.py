from django.contrib.auth.mixins import UserPassesTestMixin

from webapp.forms import DisciplineForm
from webapp.models import Discipline
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import render


class DisciplineListView(UserPassesTestMixin, ListView):
    template_name = 'disciplines/disciplines.html'
    model = Discipline
    ordering = ["name"]
    context_object_name = 'disciplines'

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class DisciplineCreateView(UserPassesTestMixin, CreateView):
    model = Discipline
    template_name = 'add.html'
    form_class = DisciplineForm

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

    def form_valid(self, form):
        text = form.cleaned_data['name']
        teacher_text = form.cleaned_data['teacher']
        print(teacher_text)
        if Discipline.objects.filter(name=text.capitalize()):
            messages.error(self.request, 'Объект с таким названием уже существует!')
            return render(self.request, 'add.html', {})
        else:
            discipline = Discipline(name=text.capitalize())
            discipline.save()
            discipline.teacher.set(teacher_text)
            discipline.save()
            return self.get_success_url()

    def get_success_url(self):
        return redirect('webapp:disciplines')


class DisciplineUpdateView(UserPassesTestMixin, UpdateView):
    model = Discipline
    template_name = 'change.html'
    form_class = DisciplineForm

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

    def get_success_url(self):
        return reverse('webapp:disciplines')


class DisciplineDeleteView(UserPassesTestMixin, DeleteView):
    model = Discipline
    template_name = 'delete.html'
    success_url = reverse_lazy('webapp:disciplines')

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

