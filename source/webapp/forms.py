from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS

from accounts.models import Profile
from .models import Schedule, Lesson


class ScheduleForm(forms.ModelForm):
    lesson = forms.ModelChoiceField(queryset=Lesson.objects.filter(is_saturday=False), label='Пара')
    teacher = forms.ModelChoiceField(queryset=User.objects.filter(profile__role__name__contains ='Преподаватель'), label='Преподаватель')

    # def __init__(self, teachers,  **kwargs):
    #     super().__init__(**kwargs)
    #     self.fields['teacher'].queryset = teachers

    # def get_initial_for_field(self, field, field_name):
    #     if 'teacher'  in self.Meta.fields:
    #         return getattr(self.instance.teacher, field_name.get_full_name())
    #     return super().get_initial_for_field(field, field_name)

    class Meta:
        model = Schedule
        fields = ['day', 'lesson', 'discipline', 'group', 'teacher', 'auditoriya']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Выберите другой день, пару или аудиторию",

            }
        }


