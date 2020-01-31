from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404

from accounts.models import Group
from webapp.models import Journal
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class JournalIndexView(ListView):
    template_name = 'journal/list.html'
    model = Journal
    context_object_name = 'journals'
    paginate_by = 30
    paginate_orphans = 0
    page_kwarg = 'page'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update({
            'groups': Group.objects.all()
        })
        return context


class JournalCreateView(CreateView):
    model = Journal
    template_name = 'add.html'
    fields = ['discipline', 'student', 'date', 'theme', 'grade']

    def get_success_url(self):
        return reverse('webapp:journal')


class GradeforStudentCreateView(CreateView):
    model = Journal
    template_name = 'add.html'
    fields = ['discipline', 'date', 'theme', 'grade']

    def dispatch(self, request, *args, **kwargs):
        self.user = self.get_user()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = self.user.student.create(**form.cleaned_data)
        return redirect('webapp:journal')

    def get_user(self):
        user_pk = self.kwargs.get('pk')
        return get_object_or_404(User, pk=user_pk)


class JournalUpdateView(UpdateView):
    model = Journal
    template_name = 'change.html'
    fields = ['theme']

    def get_success_url(self):
        return reverse('webapp:journal')


class JournalDeleteView(DeleteView):
    model = Journal
    template_name = 'delete.html'
    success_url = reverse_lazy('webapp:journal')
