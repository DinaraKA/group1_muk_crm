from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS
from .models import Schedule, Lesson, Theme


class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ['name']


class ScheduleForm(forms.ModelForm):
    lesson = forms.ModelChoiceField(queryset=Lesson.objects.filter(is_saturday=False))
    teacher = forms.ModelChoiceField(queryset=User.objects.filter(profile__role__name__contains='Преподаватель'), label='Преподаватель')

    class Meta:
        model = Schedule
        fields = ['day', 'lesson', 'discipline', 'group', 'teacher', 'auditoriya']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Выберите другой день, пару или аудиторию",

            }
        }


