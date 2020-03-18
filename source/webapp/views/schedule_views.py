from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from webapp.forms import ScheduleForm
from webapp.models import Schedule, Lesson,  DAY_CHOICES
from accounts.models import Profile, Family, StudyGroup


class ScheduleView(ListView):
    model = Schedule
    template_name = 'schedule/schedule.html'
    context_object_name = 'schedules'

    def get_context_data(self, **kwargs):
        context = super(ScheduleView, self).get_context_data(**kwargs)
        student = Family.objects.filter(family_user=self.request.user).values('student')
        context.update({
            'lessons': Lesson.objects.filter(is_saturday=False),
            'saturdaylessons': Lesson.objects.filter(is_saturday=True),
            'groups': StudyGroup.objects.filter(students=self.request.user),
            'days': DAY_CHOICES,
            'teacher': Profile.objects.filter(role__name='Преподаватель', user=self.request.user),
            'weekdays': self.get_weekdays(),
            'difference': self.get_len(),
            'family_users': Family.objects.filter(family_user=self.request.user),
            'groups_for_parent': StudyGroup.objects.filter(students__in=student),
        })
        print(Family.objects.filter(family_user=self.request.user))
        return context

    def get_len(self):
        difference = []
        lesson = len(Lesson.objects.filter(is_saturday=False))
        saturdaylesson = len(Lesson.objects.filter(is_saturday=True))
        for item in range(lesson - saturdaylesson):
            difference.append(" ")
        return difference

    def day_array(self, day):
        day_array = [[],[],[],[],[],[],[],[]]
        schedule_day = Schedule.objects.filter(day=day)
        i = 0
        while i < 9:
            try:
                index = schedule_day[i].lesson.index - 1
                day_array[index].append(schedule_day[i])
            except:
                pass
            i += 1
        return day_array

    def get_weekdays(self):
        weekdays = {}
        for day in DAY_CHOICES:
            weekdays.update({
                day[1]: self.day_array(day[0])
            })
        return weekdays

    def get_queryset(self):
        return Schedule.objects.all()


class ScheduleAddView(UserPassesTestMixin, CreateView):
    model = Schedule
    template_name = 'add.html'
    form_class = ScheduleForm

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

    def get_success_url(self):
        return reverse('webapp:schedule')


class ScheduleUpdateView(UserPassesTestMixin, UpdateView):
    model = Schedule
    template_name = 'change.html'
    form_class = ScheduleForm

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

    def get_success_url(self):
        return reverse('webapp:schedule')


class ScheduleDeleteView(UserPassesTestMixin, DeleteView):
    model = Schedule
    template_name = 'delete.html'

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

    def get_success_url(self):
        return reverse('webapp:schedule')



