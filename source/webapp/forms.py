from django import forms
from .models import Schedule, Lesson, Theme


class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ['name']


class ScheduleForm(forms.ModelForm):
    lesson = forms.ModelChoiceField(queryset=Lesson.objects.filter(is_saturday=False), label='Lesson', empty_label=None)

    class Meta:
        model = Schedule
        fields = ['lesson', 'day', 'discipline', 'group', 'teacher', 'auditoriya']

