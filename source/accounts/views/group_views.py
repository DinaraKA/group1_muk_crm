from accounts.models import Group
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class GroupListView(ListView):
    template_name = 'group/list.html'
    model = Group
    ordering = ["-name"]
    context_object_name = 'groups'
    paginate_by = 10
    paginate_orphans = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class GroupDetailView(DetailView):

    template_name = 'group/detail.html'

    model = Group


class GroupCreateView(CreateView):
    model = Group
    template_name = 'add.html'
    fields = ['name', 'students', 'starosta', 'kurator', 'started_at']

    def get_success_url(self):
        return reverse('accounts:groups')


class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'change.html'
    fields = ['name', 'students', 'starosta', 'kurator', 'started_at']  

    def get_success_url(self):
        return reverse('accounts:groups')


class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'delete.html'
    success_url = reverse_lazy('accounts:groups')