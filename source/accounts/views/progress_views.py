from django.db.models import Q
from accounts.forms import SimpleSearchForm
from accounts.models import Progress
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from webapp.views.base_views import SearchView


class ProgressIndexView(SearchView):
    template_name = 'progress/list.html'
    model = Progress
    context_object_name = 'progress'
    paginate_by = 30
    paginate_orphans = 3
    page_kwarg = 'page'
    ordering = ['-discipline']
    search_form = SimpleSearchForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        print(Progress.objects.filter(student__student_group=1))
        return context

    def get_filters(self):
        return Q(discipline__icontains=self.search_value)

class ProgressCreateView(CreateView):
    model = Progress
    template_name = 'add.html'
    fields = ['student', 'discipline']

    def get_success_url(self):
        return reverse('accounts:progress')


class ProgressUpdateView(UpdateView):
    model = Progress
    template_name = 'change.html'
    fields = ['grade']

    def get_success_url(self):
        return reverse('accounts:progress')


class ProgressDeleteView(DeleteView):
    model = Progress
    template_name = 'delete.html'
    success_url = reverse_lazy('accounts:progress')
