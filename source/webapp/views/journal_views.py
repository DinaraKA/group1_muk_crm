from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from accounts.models import StudyGroup
from webapp.models import Journal, Discipline, StudyGroup, GroupJournal, JournalNote
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView


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
        groupjournal = GroupJournal.objects.get(pk=self.kwargs['pk'])
        journalnotes = JournalNote.objects.filter(group_journal=groupjournal).order_by('date')
        context.update({
            'journalnotes': journalnotes,
        })
        return context

class GroupJournalCreateView(CreateView):
    model = GroupJournal
    template_name = 'add.html'
    fields = ['study_group','discipline']

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
    fields = ['study_group','discipline']

    def get_success_url(self):
        return reverse('webapp:groupjournals')


class GroupJournalDeleteView(DeleteView):
    model = GroupJournal
    template_name = 'delete.html'
    success_url = reverse_lazy('webapp:groupjournals')



class JournalNoteCreateView(CreateView):
    model = JournalNote
    template_name = 'add.html'
    fields = ['theme']

    def form_valid(self, form):
        self.journal_pk = self.kwargs.get('pk')
        journal = get_object_or_404(GroupJournal, pk=self.journal_pk)
        journalnote = JournalNote(
            group_journal = journal,
            theme=form.cleaned_data['theme'],
            created_by=self.request.user
        )
        journalnote.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('webapp:groupjournal', kwargs={"pk": self.journal_pk})



