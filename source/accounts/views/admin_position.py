from accounts.models import AdminPosition

from django.urls import reverse, reverse_lazy

from django.views.generic import CreateView, UpdateView, DeleteView



class AdminPositionCreateView(CreateView):
    model = AdminPosition
    template_name = 'add.html'
    fields = ['name']

    def get_success_url(self):
        return reverse('webapp:index')