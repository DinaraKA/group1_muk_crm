from django import forms
from .models import Schedule, Lesson


class ScheduleForm(forms.ModelForm):
    lesson = forms.ModelChoiceField(queryset=Lesson.objects.filter(is_saturday=False))
    class Meta:
        model = Schedule
        fields = ['lesson', 'day', 'discipline', 'group', 'teacher', 'auditoriya']


YEARS = [x for x in range(2000,2022)]


class FullSearchForm(forms.Form):
    start_date= forms.DateField(label='Введите дату начала!', widget=forms.SelectDateWidget(years=YEARS))
    end_date = forms.DateField(label='Введите дату окончания!', widget=forms.SelectDateWidget(years=YEARS))
    discipline = forms.CharField(max_length=100, required=False, label="По дисциплине")
