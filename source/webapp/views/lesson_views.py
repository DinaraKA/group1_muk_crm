from webapp.models import Lesson
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class LessonListView(ListView):
    template_name = 'lesson/all_lessons.html'
    model = Lesson
    ordering = ["start_time"]
    context_object_name = 'lessons'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data()
    #     return context