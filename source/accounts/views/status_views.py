from django.contrib.auth.mixins import PermissionRequiredMixin
from accounts.models import Status
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404,render
from django.contrib import messages


class StatusListView(PermissionRequiredMixin, ListView):
    template_name = 'status/statuses.html'
    model = Status
    ordering = ["-name"]
    context_object_name = 'statuses'
    paginate_by = 20
    paginate_orphans = 2
    permission_required = "accounts.view_status"
    permission_denied_message = "Доступ запрещен"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class StatusCreateView(PermissionRequiredMixin, CreateView):
    model = Status
    template_name = 'add.html'
    fields = ['name']
    permission_required = "accounts.add_status"

    def form_valid(self, form):
        text = form.cleaned_data['name']
        if Status.objects.filter(name=text.capitalize()):
            messages.error(self.request, 'Объект с таким названием уже существует!')
            return render(self.request, 'add.html', {})
        else:
            admin_position = Status(name=text.capitalize())
            admin_position.save()
        return self.get_success_url()

    permission_denied_message = "Доступ запрещен"

    def get_success_url(self):
        return redirect('accounts:statuses')


class StatusUpdateView(PermissionRequiredMixin, UpdateView):
    model = Status
    template_name = 'change.html'
    fields = ['name']
    permission_required = "accounts.change_status"
    permission_denied_message = "Доступ запрещен"

    def form_valid(self, form):
        text = form.cleaned_data['name']
        if Status.objects.filter(name=text.capitalize()):
            messages.error(self.request, 'Объект с таким названием уже существует!')
            return render(self.request, 'change.html', {})
        else:
            pk = self.kwargs.get('pk')
            status = get_object_or_404(Status, id=pk)
            status.name = text.capitalize()
            status.save()
        return self.get_success_url()

    def get_success_url(self):
        return redirect('accounts:statuses')


class StatusDeleteView(PermissionRequiredMixin, DeleteView):
    model = Status
    template_name = 'delete.html'
    success_url = reverse_lazy('accounts:statuses')
    permission_required = "accounts.delete_status"
    permission_denied_message = "Доступ запрещен"
