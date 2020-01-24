from accounts.models import Theme
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class ThemeListView(ListView):
    template_name = 'theme/list.html'
    model = Theme
    ordering = ["-name"]
    context_object_name = 'themes'
    paginate_by = 20
    paginate_orphans = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class ThemeCreateView(CreateView):
    model = Theme
    template_name = 'add.html'
    fields = ['name']

    def get_success_url(self):
        return reverse('accounts:themes')


class ThemeUpdateView(UpdateView):
    model = Theme
    template_name = 'change.html'
    fields = ['name']

    def get_success_url(self):
        return reverse('accounts:themes')


class ThemeDeleteView(DeleteView):
    model = Theme
    template_name = 'delete.html'
    success_url = reverse_lazy('accounts:themes')