from django import forms
<<<<<<< HEAD
from .models import Schedule, Lesson


class ScheduleForm(forms.ModelForm):
    lesson = forms.ModelChoiceField(queryset=Lesson.objects.filter(is_saturday=False))
    class Meta:
        model = Schedule
        fields = ['lesson', 'day', 'discipline', 'group', 'teacher', 'auditoriya']

=======
from .models import Theme


class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ['name']
>>>>>>> Принятие изменений с репозитория
