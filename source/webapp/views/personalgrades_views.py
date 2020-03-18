from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from accounts.models import Family
from webapp.models import JournalGrade, JournalNote, GroupJournal


class PersonalGradesDetailView(DetailView):
    template_name = 'personalgrades/student_grades.html'
    model = User


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        student = get_object_or_404(User, pk=pk)
        print(student.profile.role.all())

        student_note = JournalNote.objects.filter(journalnote_grade__student=student)
        group = student_note[0].group_journal.study_group
        discipline = student_note[0].group_journal.discipline
        disciplines = GroupJournal.objects.filter(study_group=group)
        grade_student = JournalGrade.objects.filter(student=student)
        context.update({
            'student': student,
            'family_users': Family.objects.filter(family_user=self.request.user),
            'grades': grade_student,
            'group': group,
            'student_discipline': discipline,
            'disciplines': disciplines,
        })
        return context

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')