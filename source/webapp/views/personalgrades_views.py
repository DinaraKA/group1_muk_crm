from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from webapp.models import Journal, Discipline


class PersonalGradesDetailView(DetailView):
    template_name = 'personalgrades/personalgrades.html'
    model = Journal
    ordering = ['date']
    context_object_name = 'journal'


    def get_context_data(self, **kwargs):
        context = super(PersonalGradesDetailView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        student_marks = Journal.objects.filter(student=pk)
        print(student_marks)
        student = get_object_or_404(User, pk=pk)
        disciplines_all = {}
        # disciplines = Journal.objects.filter(discipline=disciplines_all)
        for discipline_name in disciplines_all:
            disciplines_all.update({
                discipline_name[1]: self.discipline_array(discipline_name[0])
            })
            context['disciplines_all'] = disciplines_all
            # context['english'] = self.discipline_array('English')
        context.update({
            'student': student,
            'profiles': student_marks,
            'disciplines': Discipline.objects.all()

        })
        return context

    # def get_student_discipline(self, **kwargs):
    #     pk = self.kwargs.get('pk')
    #
    #     student = get_object_or_404(User, pk=pk)
    #     # print(student)
    #     disciplines = Journal.objects.filter(student__username=student)
    #     # print(disciplines)
    #     return disciplines

    def discipline_array(self):
        discipline = []



    def discipline_array(self, discipline):
        discipline_array = [[], [], [], [], [], [], [], []]
        dis_obj = Journal.objects.filter(discipline=discipline)
        i = 0
        while i < 9:
            try:
                index = int(dis_obj[i].journal.date) - 1
                discipline_array[index].append(dis_obj[i])
            except:
                pass
            i += 1
        return discipline_array

    #     # def get_context_data(self, **kwargs):
    # #     context = super(ScheduleView, self).get_context_data(**kwargs)
    #     weekdays = {}
    #     for day in DAY_CHOICES:
    #         weekdays.update({
    #             day[1]: self.day_array(day[0])
    #         })
    #     context['weekdays'] = weekdays
    #     # context["monday"] = self.day_array('Monday')
    #     # context['tuesday'] = self.day_array('Tuesday')
    #     # context['wednesday'] = self.day_array('Wednesday')
    #     # context['thursday'] = self.day_array('Thursday')
    #     # context['friday'] = self.day_array('Friday')
    #     # context['saturday'] = self.day_array('Saturday')
    #     context['groups'] = Group.objects.filter(students=self.request.user)
    #     context['teacher'] = Profile.objects.filter(role__name='Преподаватель', user__username=self.request.user)
    #     context['days'] = DAY_CHOICES
    #     context.update({
    #         'lessons': Lesson.objects.all(),
    #         # 'saturday_lesson': SaturdayLesson.objects.all(),
    #     })
    #     return context
