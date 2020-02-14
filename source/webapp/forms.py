from django import forms
from .models import Schedule, Lesson, Discipline


class ScheduleForm(forms.ModelForm):
    lesson = forms.ModelChoiceField(queryset=Lesson.objects.filter(is_saturday=False))
    class Meta:
        model = Schedule
        fields = ['lesson', 'day', 'discipline', 'group', 'teacher', 'auditoriya']


YEARS = [x for x in range(2019,2021)]


class FullSearchForm(forms.Form):
    start_date= forms.DateField(label='Введите дату начала!', widget=forms.SelectDateWidget(years=YEARS))
    end_date = forms.DateField(label='Введите дату окончания!', widget=forms.SelectDateWidget(years=YEARS))
    discipline = forms.ModelChoiceField(required=False, queryset=Discipline.objects.all(), label="По дисциплине")
