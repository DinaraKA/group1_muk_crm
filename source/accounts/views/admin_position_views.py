from django.contrib.auth.mixins import PermissionRequiredMixin
from accounts.models import AdminPosition
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.shortcuts import render


class AdminPositionIndexView(PermissionRequiredMixin, ListView):
    template_name = 'admin_position/list.html'
    model = AdminPosition
    context_object_name = 'adminpositions'
    paginate_by = 6
    paginate_orphans = 0
    page_kwarg = 'page'
    permission_required = "accounts.view_adminposition"
    permission_denied_message = "Доступ запрещен"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class AdminPositionCreateView(PermissionRequiredMixin, CreateView):
    model = AdminPosition
    template_name = 'add.html'
    fields = ['name']
    permission_required = "accounts.add_adminposition"
    permission_denied_message = "Доступ запрещен"

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


class AdminPositionUpdateView(PermissionRequiredMixin, UpdateView):
    model = AdminPosition
    template_name = 'change.html'
    fields = ['name']
    permission_required = "accounts.change_adminposition"
    permission_denied_message = "Доступ запрещен"

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


class AdminPositionDeleteView(PermissionRequiredMixin, DeleteView):
    model = AdminPosition
    template_name = 'delete.html'
    success_url = reverse_lazy('accounts:adminpositions')
    permission_required = "accounts.delete_adminposition"
    permission_denied_message = "Доступ запрещен"
