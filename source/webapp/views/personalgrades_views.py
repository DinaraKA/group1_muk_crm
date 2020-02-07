from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from webapp.forms import FullSearchForm
from webapp.models import Journal
from django.utils.http import urlencode


class PersonalGradesDetailView(DetailView):
    template_name = 'personalgrades/personalgrades.html'
    model = Journal
    ordering = ['discipline']
    context_object_name = 'journal'
    paginate_by = 5
    paginate_orphans = 1

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PersonalGradesDetailView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        student_marks = Journal.objects.filter(student=pk)
        student = get_object_or_404(User, pk=pk)
        context['form'] = self.form     # добавляю поиск
        context.update({
            'student': student,
            'profiles': student_marks,
        })
        if self.search_value:
            context['query'] = urlencode({'start_date': self.search_value, 'end_date': self.search_value})
        return context

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(object_list=object_list, **kwargs)
    #     context['form'] = self.form
    #     if self.search_value:
    #         context['query'] = urlencode({'search': self.search_value})
    #     return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = (Q(date_day=self.search_value) and Q(date__month= self.search_value) and Q(date__year=self.search_value))
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return FullSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['start_date', 'end date']
        return None

# if search_text:
#             articles = Article.objects.filter(Q(МодельСдатами__дата__year=search_text) and Q(МодельСдатами__дата__day=search_text))
