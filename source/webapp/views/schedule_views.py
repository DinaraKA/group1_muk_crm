from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from webapp.models import Schedule, Lesson, SaturdayLesson
from accounts.models import Group, User, Profile


class ScheduleView(ListView):
    model = Schedule
    template_name = 'schedule/schedule.html'
    context_object_name = 'schedules'

    def get_context_data(self, **kwargs):
        context = super(ScheduleView, self).get_context_data(**kwargs)
        context["monday"] = self.day_array('Monday')
        context['tuesday'] = self.day_array('Tuesday')
        context['wednesday'] = self.day_array('Wednesday')
        context['thursday'] = self.day_array('Thursday')
        context['friday'] = self.day_array('Friday')
        context['saturday'] = self.day_array('Saturday')
        context['groups'] = Group.objects.filter(students=self.request.user)
        context['teacher'] = Profile.objects.filter(role__name='Преподаватель', user__username=self.request.user)
        print(context['teacher'])
        context.update({
            'lessons': Lesson.objects.all(),
            'saturday_lesson': SaturdayLesson.objects.all(),
        })
        return context

    # def day_array(self, day):
    #     day_array = ["","","","","","","",""]
    #     schedule_day = Schedule.objects.filter(day=day)
    #     i = 0
    #     while i < 9:
    #         try:
    #             index = int(schedule_day[i].lesson.name) - 1
    #             day_array[index] = (schedule_day[i])
    #         except:
    #             pass
    #         i += 1
    #     return day_array

    def day_array(self, day):
        day_array = [[],[],[],[],[],[],[],[]]
        schedule_day = Schedule.objects.filter(day=day)
        i = 0
        while i < 9:
            try:
                index = int(schedule_day[i].lesson.name) - 1
                day_array[index].append(schedule_day[i])
            except:
                pass
            i += 1
        return day_array

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



