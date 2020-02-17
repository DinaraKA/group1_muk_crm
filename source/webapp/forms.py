from django import forms
from .models import Schedule, Lesson, Theme, Discipline
from django.forms import DateInput
from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS



class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ['name']


class ScheduleForm(forms.ModelForm):
    lesson = forms.ModelChoiceField(queryset=Lesson.objects.filter(is_saturday=False), label='Пара')
    teacher = forms.ModelChoiceField(queryset=User.objects.filter(profile__role__name__contains='Преподаватель'), label='Преподаватель')

    class Meta:
        model = Schedule
        fields = ['day', 'lesson', 'discipline', 'group', 'teacher', 'auditoriya']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Выберите другой день, пару или аудиторию",

            }
        }



class DateJournalInput(DateInput):
    input_type = 'date'


class FullSearchForm(forms.Form):
    start_date = forms.DateField(label='Введите дату начала', required=False, widget=DateJournalInput)
    end_date = forms.DateField(label='Введите дату окончания', required=False, widget=DateJournalInput)
    discipline = forms.ModelChoiceField(required=False, queryset=Discipline.objects.all(), label="По дисциплине")
