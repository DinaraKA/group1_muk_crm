from webapp.models import Auditory
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin


class AuditoryListView(UserPassesTestMixin, ListView):
    template_name = 'auditory/auditories.html'
    model = Auditory
    ordering = ["-name"]
    context_object_name = 'auditories'

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class AuditoryCreateView(CreateView):
    model = Auditory
    template_name = 'add.html'
    fields = ['name', 'places', 'description']

    def form_valid(self, form):
        text = form.cleaned_data['name']
        if Auditory.objects.filter(name=text.capitalize()):
            messages.error(self.request, 'Объект с таким названием уже существует!')
            return render(self.request, 'add.html', {})
        else:
            auditory = Auditory(name=text.capitalize(), places=form.cleaned_data['places'],
                                description=form.cleaned_data['description'])
            auditory.save()
        return self.get_success_url()

    def get_success_url(self):
        return redirect('webapp:auditories')


class AuditoryUpdateView(UpdateView):
    model = Auditory
    template_name = 'change.html'
    fields = ['name', 'places', 'description']

    def get_success_url(self):
        return reverse('webapp:auditories')


class AuditoryDeleteView(DeleteView):
    model = Auditory
    template_name = 'delete.html'
    success_url = reverse_lazy('webapp:auditories')

