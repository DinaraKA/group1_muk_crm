from django.contrib.auth.mixins import PermissionRequiredMixin
from accounts.models import Role
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class RoleIndexView(PermissionRequiredMixin, ListView):
    template_name = 'role/roles.html'
    model = Role
    context_object_name = 'roles'
    paginate_by = 4
    paginate_orphans = 0
    page_kwarg = 'page'
    permission_required = "accounts.view_role"
    permission_denied_message = "Доступ запрещен"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class RoleCreateView(PermissionRequiredMixin, CreateView):
    model = Role
    template_name = 'add.html'
    fields = ['name']
    permission_required = "accounts.add_role"
    permission_denied_message = "Доступ запрещен"

    def get_success_url(self):
        return reverse('accounts:roles_list')


class RoleUpdateView(PermissionRequiredMixin, UpdateView):
    model = Role
    template_name = 'change.html'
    fields = ['name']
    permission_required = "accounts.change_role"
    permission_denied_message = "Доступ запрещен"

    def get_success_url(self):
        return reverse('accounts:roles_list')


class RoleDeleteView(PermissionRequiredMixin, DeleteView):
    model = Role
    template_name = 'delete.html'
    success_url = reverse_lazy('accounts:roles_list')
    permission_required = "accounts.delete_role"
    permission_denied_message = "Доступ запрещен"
