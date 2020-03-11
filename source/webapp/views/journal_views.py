from django.template.defaulttags import register

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
        print(context,'ok')
        context['form'] = JournalNoteForm()
        context['grade_form'] = GradeForm()
        groupjournal = GroupJournal.objects.get(pk=self.kwargs['pk'])
        self.journalnotes = JournalNote.objects.filter(group_journal=groupjournal).order_by('date')
        ds = groupjournal.discipline
        print(ds,'to')
        students = groupjournal.study_group.students.all().order_by('last_name')
        studentsgr = []

        for st in students:
            one_student_grades = st.student_grade.filter(journal_note__group_journal__discipline=ds)
            sum = 0
            count = 0
            abs = 0
            for grade in one_student_grades:
                print(grade.grade.value, 'u')
                if grade.grade.value != 'нб':
                    sum += int(grade.grade.value)
                    count += 1
                else:
                    abs +=1
            if count != 0:
                avg=sum/count
            else:
                avg = 0
                    # print(sum,'d', count)
            studentsgr.append({
                st.id: {
                    'avg': avg,
                    'abs': abs
                }
            })

            # return sum
            print('next_student')
        print(studentsgr)
        # test = JournalGrade.avg_grade(self, student=27)
        # context['avg'] = self.group_st(groupjournal)
        # test = self.avg_grade()
        # print(test)

        # for obj in self.journalnotes:
        #     # test=[]
        #     # test.append(obj.journalnote_grade.values('grade'))
        #     print(obj.journalnote_grade.val)

        # for object in journalnotes:
        #     obj = object.pk
        #     print(object)
        #     journalgrade = JournalGrade.objects.filter(journal_note=obj)
        #
        #     print(journalgrade)
        context.update({
            'journalnotes': self.journalnotes,
            'avg': studentsgr
            # 'grade': journalgrade
            # 'obj': obj
        })
        return context

    # def avg_grade(self, student, discipline):
    #     # grades = Grade.objects.filter(note_grade__journal_note__group_journal=group)
    #     grades = JournalGrade.objects.filter(student=27, journal_note__group_journal__discipline=discipline)
    #     print(grades)
    #     count = 0
    #     if grades:
    #         for grade in grades.values_list('grade__value', flat=None):
    #             print(grade)
    #             count += int(grade)
    #             print(count,'t')
    #         return count
    #         avg = count / len(grades)
    #         avg_grade = round(avg, 1)
    #     return avg_grade
    #
    # def group_st(self, obj):
    #     st = obj.study_group.students.all()
    #     print(st, 'yes')
    #     for student in st:
    #         print(student.pk,'s')
    #         return self.avg_grade(student=student.pk, discipline=obj.discipline)



    # def avg_grade(self):
    #     for student in self.groupjournal.study_group.students.all():
    #
    #         self.grades = JournalGrade.objects.filter(student_id=student, journal_note__group_journal=self.groupjournal)
    #         # print(self.grades)
    #         # return self.grades
    #     # for obj in self.journalnotes:
    #     #     # test=[]
    #     #     # test.append(obj.journalnote_grade.values('grade'))
    #     #     print(obj.journalnote_grade.values_list('grade'))
    #     # # grades = JournalGrade.objects.filter(student_id=)
    # # def avg_grade(self):
    #     count = 0
    #     grades = Grade.objects.filter(value=)
    #     for grade in grades:
    #         print('yes')
    #         print(grade)
    #         # test = Grade.objects.get(value=grade)
    #         # print(test.value)
    #         count += int(grade)
    #         # print(count)
    #         avg = count / len(grades)
    #         avg_grade = round(avg, 1)
    #         # print(avg_grade)
    #         return avg_grade
# @register.filter(name='lookup')
# def lookup(value, arg):
#     return value[arg]

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


class JournalSelectView(FormView):
    template_name = 'journal/journal_select.html'
    form_class = JournalSelectForm

    def form_valid(self, form):
        group = form.cleaned_data.get('study_group')
        discipline = form.cleaned_data.get('discipline')
        journal_obj = GroupJournal.objects.get(study_group=group, discipline=discipline)
        return redirect('webapp:groupjournal', pk=journal_obj.id)
