from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from accounts.models import StudyGroup
from webapp.forms import JournalNoteForm, GradeForm, JournalSelectForm
from webapp.models import Discipline, StudyGroup, GroupJournal, JournalNote, JournalGrade, Grade
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View, TemplateView, FormView
from django.utils.http import urlencode


class GroupJournalListView(ListView):
    model = GroupJournal
    template_name = 'journal/group_journals_list.html'
    context_object_name = 'groupjournals'
    ordering = ['study_group']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class GroupJournalDetailView(DetailView):
    template_name = 'journal/group_journal.html'
    model = GroupJournal
    context_object_name = 'journal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = JournalNoteForm()
        context['grade_form'] = GradeForm()
        groupjournal = GroupJournal.objects.get(pk=self.kwargs['pk'])
        journalnotes = JournalNote.objects.filter(group_journal=groupjournal).order_by('date')
        # for object in journalnotes:
        #     obj = object.pk
        #     print(object)
        #     journalgrade = JournalGrade.objects.filter(journal_note=obj)
        #
        #     print(journalgrade)
        context.update({
            'journalnotes': journalnotes,
            # 'grade': journalgrade
            # 'obj': obj
        })
        return context


class GroupJournalCreateView(CreateView):
    model = GroupJournal
    template_name = 'add.html'
    fields = ['study_group', 'discipline']

    def get_success_url(self):
        return reverse('webapp:groupjournals')

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data()
    #     context.update({
    #         'groups': StudyGroup.objects.all(),
    #         'disciplines': Discipline.objects.all()
    #     })
    #     return context


class GroupJournalUpdateView(UpdateView):
    model = GroupJournal
    template_name = 'change.html'
    fields = ['study_group', 'discipline']

    def get_success_url(self):
        return reverse('webapp:groupjournals')


class GroupJournalDeleteView(DeleteView):
    model = GroupJournal
    template_name = 'delete.html'
    success_url = reverse_lazy('webapp:groupjournals')


class JournalNoteCreateView(CreateView):
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
        # return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('webapp:groupjournal', kwargs={"pk": self.journal_pk})


class JournalGradeCreateView(CreateView):
    model = JournalGrade
    form_class = GradeForm

    def post(self, request, *args, **kwargs):
        self.student_pk = self.kwargs.get('pk')
        self.journal_note_pk = self.request.POST.get("student_" + str(self.student_pk), None)
        self.journal_note_obj = JournalNote.objects.get(id=self.journal_note_pk)
        form = self.form_class(self.request.POST)

        # grade_obj = Grade.objects.get(form.save(commit=False))
        # obj_grade, created = JournalGrade.objects.get_or_create(journal_note=self.journal_note_obj, student=self.student_obj, **kwargs)
        # print('no')
        # print(obj_grade)
        # if created != True:
        #     if form.is_valid():
        #         print('yes')
        #         obj = form.save(commit=False)
        #         obj.student_id = self.student_pk
        #         obj.journal_note_id = self.journal_note_pk
        #         obj.created_by = self.request.user
        #         obj.save()
        #         return redirect('webapp:groupjournal', pk=self.journal_note_obj.group_journal_id)
        # else:
        #     print('yes')
        #     form_grade = self.request.POST.get('grade', None)
        #     grade = Grade.objects.get(value=form_grade)
        #     obj_grade.grade = grade
        #     obj_grade.save()
        #     return redirect('webapp:groupjournal', pk=self.journal_note_obj.group_journal_id)
        try:
            obj_grade, _ = JournalGrade.objects.get_or_create(journal_note_id=self.journal_note_pk, student_id=self.student_pk)
            if obj_grade:
                form_grade = self.request.POST.get('grade', None)
                grade = Grade.objects.get(value=form_grade)
                obj_grade.grade = grade
                obj_grade.save()
                return redirect('webapp:groupjournal',pk=self.journal_note_obj.group_journal_id)
        except:
            if form.is_valid():
                obj = form.save(commit=False)
                obj.student_id = self.student_pk
                obj.journal_note_id = self.journal_note_pk
                obj.created_by = self.request.user
                obj.save()
                return redirect('webapp:groupjournal',pk=self.journal_note_obj.group_journal_id)
        # else:
        #     print('yes')
        #     form_grade = self.request.POST.get('grade', None)
        #     grade = Grade.objects.get(value=form_grade)
        #     obj_grade.grade = grade
        #     obj_grade.save()
        #     return redirect('webapp:groupjournal', pk=self.journal_note_obj.group_journal_id)

    # def form_valid(self, form):
    #     # self.journalnote_pk = self.kwargs.get('pk')
    #     self.student_pk = self.kwargs.get('pk')
    #     # self.journal_pk = self.kwargs.get('pk')
    #     # print(self.journal_pk)
    #     print(self.student_pk)
    #     # journalnote = get_object_or_404(JournalNote, pk=self.journalnote_pk)
    #     journalnote = JournalGrade.objects.filter(student=self.student_pk)
    #     print(journalnote)
    #     student = get_object_or_404(User, pk= self.student_pk)
    #     journalgrade = JournalGrade(
    #         journal_note = journalnote,
    #         grade=form.cleaned_data['grade'],
    #         created_by=self.request.user,
    #         description=form.cleaned_data['description'],
    #         student= student
    #     )
    #     journalgrade.save()
    #     # return redirect('webapp:groupjournal', pk=self.journal_pk)
    #     return HttpResponseRedirect(self.get_success_url())

# class JournalSelectView(TemplateView):
#     template_name = 'journal/journal_select.html'
#     form_class = JournalSelectForm
#

class JournalSelectView(FormView):
    template_name = 'journal/journal_select.html'
    form_class = JournalSelectForm

    def form_valid(self, form):
        group = form.cleaned_data.get('study_group')
        discipline = form.cleaned_data.get('discipline')
        journal_obj = GroupJournal.objects.get(study_group=group, discipline=discipline)
        return redirect('webapp:groupjournal',pk=journal_obj.id)