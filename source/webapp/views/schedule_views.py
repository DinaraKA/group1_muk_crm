from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from webapp.models import Schedule, Lesson


class ScheduleView(ListView):
    model = Schedule
    template_name = 'schedule/schedule.html'
    context_object_name = 'schedules'

    def get_context_data(self, **kwargs):
        context = super(ScheduleView, self).get_context_data(**kwargs)
        monday_array = ["","","","","","","",""]
        shedule_monday = Schedule.objects.filter(day="Monday")
        i = 0
        while i < 9:
            try:
                index = int(shedule_monday[i].lesson.name) - 1
                monday_array[index] = (shedule_monday[i])
            except:
                pass
            i += 1
        context["monday"] = monday_array

        context.update({
            'lessons': Lesson.objects.all()
        })
        return context

    def get_queryset(self):
        return Schedule.objects.all()

class ScheduleAddView(CreateView):
    model = Schedule
    template_name = 'add.html'
    fields = ['lesson', 'day', 'discipline', 'group', 'teacher', 'auditoriya']


    def get_success_url(self):
        return reverse('webapp:schedule')


class ScheduleUpdateView(UpdateView):
    model = Schedule
    template_name = 'change.html'
    fields = ['lesson', 'day', 'discipline', 'group', 'teacher', 'auditoriya']


    def get_success_url(self):
        return reverse('webapp:schedule')


class ScheduleDeleteView(DeleteView):
    model = Schedule
    template_name = 'delete.html'

    def get_success_url(self):
        return reverse('webapp:schedule')



