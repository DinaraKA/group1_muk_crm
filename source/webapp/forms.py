from django import forms
from .models import Schedule, Lesson, Discipline
from django.forms import DateInput


class ScheduleForm(forms.ModelForm):
    lesson = forms.ModelChoiceField(queryset=Lesson.objects.filter(is_saturday=False))
    class Meta:
        model = Schedule
        fields = ['lesson', 'day', 'discipline', 'group', 'teacher', 'auditoriya']


class DateJournalInput(DateInput):
    input_type = 'date'


class FullSearchForm(forms.Form):
    start_date = forms.DateField(label='Введите дату начала', required=False, widget=DateJournalInput)
    end_date = forms.DateField(label='Введите дату окончания', required=False, widget=DateJournalInput)
    discipline = forms.ModelChoiceField(required=False, queryset=Discipline.objects.all(), label="По дисциплине")
