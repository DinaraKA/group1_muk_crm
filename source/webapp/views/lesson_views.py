from django.contrib.auth.mixins import UserPassesTestMixin
from webapp.models import Lesson
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class LessonListView(UserPassesTestMixin, ListView):
    template_name = 'lesson/all_lessons.html'
    model = Lesson
    ordering = ["start_time"]

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

    def get_context_data(self, **kwargs):
        context = super(LessonListView, self).get_context_data(**kwargs)
        context.update({
            'lessons': Lesson.objects.filter(is_saturday=False)
        })
        context.update({
            'saturdaylessons': Lesson.objects.filter(is_saturday=True)
        })
        return context


class LessonCreateView(UserPassesTestMixin, CreateView):
    model = Lesson
    template_name = 'add.html'
    fields = ['index', "is_saturday", "start_time", "end_time"]
    success_url = reverse_lazy('webapp:lessons')

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')


class LessonUpdateView(UserPassesTestMixin, UpdateView):
    model = Lesson
    template_name = 'change.html'
    fields = ['index', "is_saturday", "start_time", "end_time"]
    success_url = reverse_lazy('webapp:lessons')

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')


class LessonDeleteView(UserPassesTestMixin, DeleteView):
    model = Lesson
    template_name = 'delete.html'
    success_url = reverse_lazy('webapp:lessons')

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')