from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
# from django.utils import dateformat

from accounts.models import Family
from webapp.forms import FullSearchForm
from webapp.models import JournalGrade, JournalNote, GroupJournal, Discipline, Journal


class PersonalGradesDetailView(DetailView):
    # template_name = 'personalgrades/personalgrades.html'
    template_name = 'personalgrades/student_grades.html'
    model = JournalGrade
    # ordering = ['discipline']


    # def get(self, request, *args, **kwargs):
    #     self.form = self.get_search_form()
    #     return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        student = get_object_or_404(User, pk=pk)
        student_note = JournalNote.objects.filter(journalnote_grade__student=student)
        group = student_note[0].group_journal.study_group
        discipline = student_note[0].group_journal.discipline
        disciplines = GroupJournal.objects.filter(study_group=group)
        # grade_student= GroupJournal.objects.filter(group_journal_note__journalnote_grade__student=student)
        grade_student = JournalGrade.objects.filter(student=student)
        # student_marks = self.search_queryset()
        # context['form'] = self.form     # добавляю поиск
        context.update({
            'student': student,
            # 'profiles': student_marks,
            'family_users': Family.objects.filter(family_user=self.request.user),
            'grades': grade_student,
            'group': group,
            'student_discipline': discipline,
            'disciplines': disciplines,
        })
        return context

    # def search_queryset(self):
    #     pk = self.kwargs.get('pk')
    #     self.form = self.get_search_form()
    #     if self.form.is_valid():
    #         start_date = self.form.cleaned_data['start_date']
    #         end_date = self.form.cleaned_data['end_date']
    #         # group_journal = self.form.cleaned_data['group_journal']
    #         discipline = self.form.cleaned_data['discipline']
    #         if self.form.cleaned_data['discipline'] != None:
    #             return JournalGrade.objects.filter(student=pk, date__range=(start_date, end_date), journal_note__group_journal__discipline=discipline)
    #         else:
    #             # print('test')
    #             return JournalGrade.objects.filter(student=pk, date__range=(start_date, end_date))
    #                    # and GroupJournal.objects.filter(discipline=discipline)
    #     else:
    #         # print('yes')
    #         return JournalGrade.objects.filter(student=pk)
    #
    # def get_search_form(self):
    #     return FullSearchForm(self.request.GET)

