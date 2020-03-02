from accounts.forms import GroupForm, StudentAddStudyGroupForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from accounts.models import StudyGroup, User
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect

class GroupListView(PermissionRequiredMixin, ListView):
    template_name = 'group/list.html'
    model = StudyGroup
    ordering = ["-name"]
    context_object_name = 'group_list'
    paginate_by = 10
    paginate_orphans = 2
    permission_required = "accounts.view_group"
    permission_denied_message = "Доступ запрещен"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class GroupDetailView(PermissionRequiredMixin, DetailView):
    template_name = 'group/detail.html'
    model = StudyGroup
    context_object_name = 'group'
    permission_required = "accounts.view_group"
    permission_denied_message = "Доступ запрещен"


class GroupCreateView(PermissionRequiredMixin, CreateView):
    model = StudyGroup
    template_name = 'add.html'
    # fields = ['name', 'students', 'group_leader', 'head_teacher', 'started_at']
    permission_required = "accounts.add_group"
    permission_denied_message = "Доступ запрещен"
    form_class = GroupForm

    def form_valid(self, form):
        text = form.cleaned_data['name']
        if StudyGroup.objects.filter(name=text.capitalize()):
            messages.error(self.request, 'Объект с таким названием уже существует!')
            return render(self.request, 'add.html', {})
        else:
            group = StudyGroup(name=text.capitalize(),
                               group_leader=form.cleaned_data['group_leader'],
                               head_teaher=form.cleaned_data['head_teacher'],
                               started_at=form.cleaned_data['started_at'])
            students = form.cleaned_data['students']
            print(students)
            group.save()
            group.students.set(students)
            # group.head_teaher.set(form.cleaned_data['head_teacher'])
        return self.get_success_url()

    def get_success_url(self):
        return redirect('accounts:groups')


class GroupUpdateView(PermissionRequiredMixin, UpdateView):
    model = StudyGroup
    template_name = 'change.html'
    fields = ['name', 'students', 'group_leader', 'head_teaher', 'started_at']
    permission_required = "accounts.change_group"
    permission_denied_message = "Доступ запрещен"
    # form_class = GroupForm

    def get_success_url(self):
        return reverse('accounts:groups')


class GroupDeleteView(PermissionRequiredMixin, DeleteView):
    model = StudyGroup
    template_name = 'delete.html'
    success_url = reverse_lazy('accounts:groups')
    permission_required = "accounts.delete_group"
    permission_denied_message = "Доступ запрещен"


class GroupStudentAdd(UpdateView):
    model = StudyGroup
    template_name = 'group/group_student_add.html'
    form_class = StudentAddStudyGroupForm
    permission_required = "accounts.change_group"
    permission_denied_message = "Доступ запрещен"

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.filter(pk=self.kwargs['pk'])
        groups = StudyGroup.objects.all()
        context.update({
            'user': user,
            'groups': groups,
        })
        return context

    def form_valid(self, form):
        self.student_pk = self.kwargs['pk']
        text = form.cleaned_data['group_name']
        user = User.objects.filter(pk=self.kwargs['pk'])
        group_name = get_object_or_404(StudyGroup, name=text)
        group_name.students.set(user)
        group_name.save()
        return self.get_success_url()

    def get_success_url(self):
        return redirect('accounts:user_detail', pk=self.student_pk)
        # return redirect('accounts:groups')


