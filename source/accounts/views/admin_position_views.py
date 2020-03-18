from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from accounts.models import AdminPosition
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.shortcuts import render


class AdminPositionIndexView(UserPassesTestMixin, ListView):
    template_name = 'admin_position/admin_positions.html'
    model = AdminPosition
    context_object_name = 'adminpositions'
    page_kwarg = 'page'

    def test_func(self):
        user_requesting = self.request.user
        user_detail = User.objects.get(pk=self.kwargs['pk'])
        return user_requesting.is_staff or user_requesting.groups.filter(name='principal_staff')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class AdminPositionCreateView(UserPassesTestMixin, CreateView):
    model = AdminPosition
    template_name = 'add.html'
    fields = ['name']

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

    def form_valid(self, form):
        text = form.cleaned_data['name']
        if AdminPosition.objects.filter(name=text.capitalize()):
            messages.error(self.request, 'Объект с таким названием уже существует!')
            return render(self.request, 'add.html', {})
        else:
            admin_position = AdminPosition(name=text.capitalize())
            admin_position.save()
        return self.get_success_url()

    def get_success_url(self):
        return redirect('accounts:adminpositions')


class AdminPositionUpdateView(UserPassesTestMixin, UpdateView):
    model = AdminPosition
    template_name = 'change.html'
    fields = ['name']

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

    def form_valid(self, form):
        text = form.cleaned_data['name']
        if AdminPosition.objects.filter(name=text.capitalize()):
            messages.error(self.request, 'Объект с таким названием уже существует!')
            return render(self.request, 'change.html', {})
        else:
            pk = self.kwargs.get('pk')
            admin_position = get_object_or_404(AdminPosition, id=pk)
            admin_position.name = text.capitalize()
            admin_position.save()
        return self.get_success_url()

    def get_success_url(self):
        return redirect('accounts:adminpositions')


class AdminPositionDeleteView(UserPassesTestMixin, DeleteView):
    model = AdminPosition
    template_name = 'delete.html'
    success_url = reverse_lazy('accounts:adminpositions')
    permission_required = "accounts.delete_adminposition"
    permission_denied_message = "Доступ запрещен"

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

