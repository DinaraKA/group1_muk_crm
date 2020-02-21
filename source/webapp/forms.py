from django import forms
from .models import Schedule, Lesson, Discipline, Theme
from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS
from bootstrap_datepicker_plus import DatePickerInput



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


class FullSearchForm(forms.Form):
    start_date = forms.DateField(label='введите дату начала', widget=DatePickerInput(format='%d/%m/%Y'), required=False)
    end_date = forms.DateField(label='введите дату окончания', widget=DatePickerInput(format='%d/%m/%Y'), required=False)
    discipline = forms.ModelChoiceField(required=False, queryset=Discipline.objects.all(), label="По дисциплине",  widget=forms.Select
                           (attrs={'class':'form-control'}))



class DisciplineForm(forms.ModelForm):
    teacher = forms.ModelMultipleChoiceField(queryset=User.objects.filter(profile__role__name__contains='Преподаватель'), label='Преподаватель')

    class Meta:
        model = Discipline
        fields = ['name', 'teacher']

