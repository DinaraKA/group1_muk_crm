from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from webapp.models import Lesson, SaturdayLesson
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class LessonListView(ListView):
    template_name = 'lesson/all_lessons.html'
    model = Lesson
    ordering = ["start_time"]

    def get_context_data(self, **kwargs):
        context = super(LessonListView, self).get_context_data(**kwargs)
        context.update({
            'lessons': Lesson.objects.filter(is_saturday=False)
        })
        context.update({
            'saturdaylessons': Lesson.objects.filter(is_saturday=True)
        })
        return context


class LessonCreateView(CreateView):
    model = Lesson
    template_name = 'add.html'
    fields = ['index', "is_saturday", "start_time", "end_time"]
    success_url = reverse_lazy('webapp:lessons')


class LessonUpdateView(UpdateView):
    model = Lesson
    template_name = 'change.html'
    fields = ['index', "is_saturday", "start_time", "end_time"]
    success_url = reverse_lazy('webapp:lessons')


class LessonDeleteView(DeleteView):
    model = Lesson
    template_name = 'delete.html'
    success_url = reverse_lazy('webapp:lessons')


class SaturdayLessonCreateView(CreateView):
    model = SaturdayLesson
    template_name = 'add.html'
    fields = ['name', "start_time", "end_time"]
    success_url = reverse_lazy('webapp:lessons')


class SaturdayLessonUpdateView(UpdateView):
    model = SaturdayLesson
    template_name = 'change.html'
    fields = ['name', "start_time", "end_time"]
    success_url = reverse_lazy('webapp:lessons')


class SaturdayLessonDeleteView(DeleteView):
    model = SaturdayLesson
    template_name = 'delete.html'
    success_url = reverse_lazy('webapp:lessons')


