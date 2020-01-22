from webapp.models import Lesson
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class LessonListView(ListView):
    template_name = 'lesson/all_lessons.html'
    model = Lesson
    ordering = ["start_time"]
    context_object_name = 'lessons'


class LessonCreateView(CreateView):
    model = Lesson
    template_name = 'add.html'
    fields = ['name', "start_time", "end_time"]

    def get_success_url(self):
        return reverse('lessons')


class LessonUpdateView(UpdateView):
    model = Lesson
    template_name = 'change.html'
    fields = ['name', "start_time", "end_time"]

    def get_success_url(self):
        return reverse('lessons')


class LessonDeleteView(DeleteView):
    model = Lesson
    template_name = 'delete.html'
    success_url = reverse_lazy('lessons')

