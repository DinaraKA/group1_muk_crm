from urllib import request

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from isoweek import Week
from accounts.models import Profile
from webapp.models import Journal, Discipline


class PersonalGradesListView(DetailView):
    template_name = 'personalgrades/personalgrades.html'
    model = Journal
    ordering = ['date']
    context_object_name = 'journal'


    def get_context_data(self, **kwargs):
        context = super(PersonalGradesListView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        student_marks = Journal.objects.filter(student=pk)
        student = get_object_or_404(User, pk=pk)
        context.update({
            'student': student,
            'profiles': student_marks,
           'disciplines': Discipline.objects.all(),

        })
        return context
