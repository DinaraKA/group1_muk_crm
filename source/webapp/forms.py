from django import forms
from .models import Schedule, Lesson


class ScheduleForm(forms.ModelForm):
    lesson = forms.ModelChoiceField(queryset=Lesson.objects.filter(is_saturday=False))
    class Meta:
        model = Schedule
        fields = ['lesson', 'day', 'discipline', 'group', 'teacher', 'auditoriya']

