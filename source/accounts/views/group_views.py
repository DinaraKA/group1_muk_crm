from accounts.forms import GroupForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from accounts.models import Group
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class GroupListView(PermissionRequiredMixin, ListView):
    template_name = 'group/list.html'
    model = Group
    ordering = ["-name"]
    context_object_name = 'groups'
    paginate_by = 10
    paginate_orphans = 2
    permission_required = "accounts.view_group"
    permission_denied_message = "Доступ запрещен"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class GroupDetailView(PermissionRequiredMixin, DetailView):
    template_name = 'group/detail.html'
    model = Group
    permission_required = "accounts.view_group"
    permission_denied_message = "Доступ запрещен"


class GroupCreateView(PermissionRequiredMixin, CreateView):
    model = Group
    template_name = 'add.html'
    fields = ['name', 'students', 'starosta', 'kurator', 'started_at']
    permission_required = "accounts.add_group"
    permission_denied_message = "Доступ запрещен"
    form_class = GroupForm

    def get_success_url(self):
        return reverse('accounts:groups')


class GroupUpdateView(PermissionRequiredMixin, UpdateView):
    model = Group
    template_name = 'change.html'
    fields = ['name', 'students', 'starosta', 'kurator', 'started_at']
    permission_required = "accounts.change_group"
    permission_denied_message = "Доступ запрещен"
    form_class = GroupForm

    def get_success_url(self):
        return reverse('accounts:groups')


class GroupDeleteView(PermissionRequiredMixin, DeleteView):
    model = Group
    template_name = 'delete.html'
    success_url = reverse_lazy('accounts:groups')
    permission_required = "accounts.delete_group"
    permission_denied_message = "Доступ запрещен"
