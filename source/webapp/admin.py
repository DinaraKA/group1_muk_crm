from django.contrib import admin
from webapp.models import News, Announcements, Auditory, Grade, Discipline, Lesson, Schedule

admin.site.register(News)
admin.site.register(Announcements)
admin.site.register(Auditory)
admin.site.register(Grade)
admin.site.register(Discipline)
admin.site.register(Lesson)

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'day', 'group', 'teacher', 'discipline', 'auditoriya']

admin.site.register(Schedule)
