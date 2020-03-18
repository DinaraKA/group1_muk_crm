from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from webapp.forms import JournalNoteForm, GradeForm, JournalSelectForm
from webapp.models import GroupJournal, JournalNote, JournalGrade, Grade
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from django.contrib import messages


class GroupJournalListView(UserPassesTestMixin, ListView):
    model = GroupJournal
    template_name = 'journal/group_journals_list.html'
    context_object_name = 'groupjournals'
    ordering = ['study_group']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')


class GroupJournalDetailView(UserPassesTestMixin, DetailView):
    template_name = 'journal/group_journal.html'
    model = GroupJournal
    context_object_name = 'journal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = JournalNoteForm()
        context['grade_form'] = GradeForm()
        groupjournal = GroupJournal.objects.get(pk=self.kwargs['pk'])
        journalnotes = JournalNote.objects.filter(group_journal=groupjournal).order_by('date')
        students = groupjournal.study_group.students.all().order_by('last_name')
        student_values = []
        for student in students:
            one_student_grades = student.student_grade.filter(journal_note__group_journal__discipline=groupjournal.discipline)
            sum = 0
            count = 0
            abs = 0
            for grade in one_student_grades:
                if grade.grade.value != 'нб':
                    sum += int(grade.grade.value)
                    count += 1
                else:
                    abs +=1
            if count != 0:
                avg=round(sum/count,2)
            else:
                avg = 0
            student_values.append({
                student.id: {
                    'avg': avg,
                    'abs': abs
                }
            })
        context.update({
            'journalnotes': journalnotes,
            'student_grades': student_values
        })
        return context

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='teachers') or user.groups.filter(name='group_leaders') or user.groups.filter(name='principal_staff')


class GroupJournalCreateView(UserPassesTestMixin, CreateView):
    model = GroupJournal
    template_name = 'add.html'
    fields = ['study_group', 'discipline']
    permission_required = "webapp.add_group_journal"
    permission_denied_message = "Доступ запрещен"

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

    def form_valid(self, form):
        text = form.cleaned_data['discipline']
        group = form.cleaned_data['study_group']
        if GroupJournal.objects.filter(discipline=text, study_group=group):
            messages.error(self.request, 'Объект с таким названием уже существует!')
            return render(self.request, 'add.html', {})
        else:
            discipline = GroupJournal(study_group=group, discipline=text)
            discipline.save()
        return self.get_success_url()

    def get_success_url(self):
        return redirect('webapp:groupjournals')


class GroupJournalUpdateView(UserPassesTestMixin, UpdateView):
    model = GroupJournal
    template_name = 'change.html'
    fields = ['study_group', 'discipline']


    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

    def get_success_url(self):
        return reverse('webapp:groupjournals')


class GroupJournalDeleteView(UserPassesTestMixin, DeleteView):
    model = GroupJournal
    template_name = 'delete.html'
    success_url = reverse_lazy('webapp:groupjournals')


    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')


class JournalNoteCreateView(UserPassesTestMixin, CreateView):
    template_name = 'add.html'
    form_class = JournalNoteForm

    def form_valid(self, form):
        self.journal_pk = self.kwargs.get('pk')
        journal = get_object_or_404(GroupJournal, pk=self.journal_pk)
        journalnote = JournalNote(
            group_journal=journal,
            theme=form.cleaned_data['theme'],
            created_by=self.request.user
        )
        journalnote.save()
        return redirect('webapp:groupjournal', pk=self.journal_pk)

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='teachers') or user.groups.filter(name='principal_staff')

    def get_success_url(self):
        return reverse('webapp:groupjournal', kwargs={"pk": self.journal_pk})


class JournalGradeCreateView(UserPassesTestMixin, CreateView):
    model = JournalGrade
    form_class = GradeForm

    def post(self, request, *args, **kwargs):
        self.student_pk = self.kwargs.get('pk')
        self.journal_note_pk = self.request.POST.get("student_" + str(self.student_pk), None)
        self.journal_note_obj = JournalNote.objects.get(id=self.journal_note_pk)
        form = self.form_class(self.request.POST)
        obj_grade = JournalGrade.objects.filter(journal_note_id=self.journal_note_pk,
                                                student_id=self.student_pk).first()
        if obj_grade != None:
            form_grade = self.request.POST.get('grade', None)
            grade = Grade.objects.get(pk=form_grade)
            obj_grade.grade = grade
            obj_grade.save()
            return redirect('webapp:groupjournal', pk=self.journal_note_obj.group_journal_id)
        else:
            if form.is_valid():
                obj = form.save(commit=False)
                obj.student_id = self.student_pk
                obj.journal_note_id = self.journal_note_pk
                obj.created_by = self.request.user
                obj.save()
                return redirect('webapp:groupjournal', pk=self.journal_note_obj.group_journal_id)

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='teachers') or user.groups.filter(name='principal_staff')


class JournalSelectView(FormView):
    template_name = 'journal/journal_select.html'
    form_class = JournalSelectForm

    def form_valid(self, form):
        group = form.cleaned_data.get('study_group')
        discipline = form.cleaned_data.get('discipline')
        journal_obj = GroupJournal.objects.get(study_group=group, discipline=discipline)
        return redirect('webapp:groupjournal', pk=journal_obj.id)
