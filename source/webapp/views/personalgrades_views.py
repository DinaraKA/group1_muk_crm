from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from webapp.models import Journal


class PersonalGradesDetailView(DetailView):
    template_name = 'personalgrades/personalgrades.html'
    model = Journal
    ordering = ['discipline']
    context_object_name = 'journal'


    def get_context_data(self, **kwargs):
        context = super(PersonalGradesDetailView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        student_marks = Journal.objects.filter(student=pk)
        student = get_object_or_404(User, pk=pk)
        context.update({
            'student': student,
            'profiles': student_marks,
        })
        return context
#
# class PersonalGradesDetailView(SingleTableView):
#     model = Journal
#     template_name = 'personalgrades/personalgrades.html'
#     context_object_name = 'journal'
#     table_class = PersonalGradesTable
#
#     def get_queryset(self):
#         pk = self.kwargs.get('pk')
#         student = Journal.objects.filter(student=pk)
#         return student
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         pk = self.kwargs.get('pk')
#         student = get_object_or_404(User, pk=pk)
#         context['student'] = student
#         return context

