from accounts.models import AdminPosition

from django.urls import reverse, reverse_lazy

from django.views.generic import CreateView, UpdateView, DeleteView


class AdminPositionCreateView(CreateView):
    model = AdminPosition
    template_name = 'add.html'
    fields = ['name']

    def get_success_url(self):
        return reverse('webapp:index')


class AdminPositionUpdateView(UpdateView):
    model = AdminPosition
    template_name = 'change.html'
    fields = ['name']

    def get_success_url(self):
        return reverse('webapp:index')


class AdminPositionDeleteView(DeleteView):
    model = AdminPosition
    template_name = 'delete.html'
    success_url = reverse_lazy('webapp:index')
