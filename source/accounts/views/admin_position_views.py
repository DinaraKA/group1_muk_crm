from accounts.models import AdminPosition
from django.urls import reverse, reverse_lazy
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class AdminPositionIndexView(ListView):
    template_name = 'admin_position/list.html'
    model = AdminPosition
    context_object_name = 'positions'
    paginate_by = 6
    paginate_orphans = 0
    page_kwarg = 'page'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


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
