from django.contrib.auth.mixins import PermissionRequiredMixin
from accounts.models import SocialStatus
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class SocialStatusListView(PermissionRequiredMixin, ListView):
    template_name = 'social_status/all_statuses.html'
    model = SocialStatus
    ordering = ["-name"]
    context_object_name = 'statuses'
    paginate_by = 20
    paginate_orphans = 2
    permission_required = "accounts.view_socialstatus"
    permission_denied_message = "Доступ запрещен"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class SocialStatusCreateView(PermissionRequiredMixin, CreateView):
    model = SocialStatus
    template_name = 'add.html'
    fields = ['name']
    permission_required = "accounts.add_socialstatus"
    permission_denied_message = "Доступ запрещен"

    def get_success_url(self):
        return reverse('accounts:all_social_statuses')


class SocialStatusUpdateView(PermissionRequiredMixin, UpdateView):
    model = SocialStatus
    template_name = 'change.html'
    fields = ['name']
    permission_required = "accounts.change_socialstatus"
    permission_denied_message = "Доступ запрещен"

    def get_success_url(self):
        return reverse('accounts:all_social_statuses')


class SocialStatusDeleteView(PermissionRequiredMixin, DeleteView):
    model = SocialStatus
    template_name = 'delete.html'
    success_url = reverse_lazy('accounts:all_social_statuses')
    permission_required = "accounts.delete_socialstatus"
    permission_denied_message = "Доступ запрещен"
