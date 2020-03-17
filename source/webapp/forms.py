from django import forms

from accounts.models import StudyGroup
from .models import Schedule, Lesson, Discipline, JournalNote, JournalGrade, GroupJournal
from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS
from bootstrap_datepicker_plus import DatePickerInput



class ScheduleForm(forms.ModelForm):
    lesson = forms.ModelChoiceField(queryset=Lesson.objects.filter(is_saturday=False), label='Пара')
    teacher = forms.ModelChoiceField(queryset=User.objects.filter(profile__role__name__contains='Преподаватель'), label='Преподаватель')

    def clean(self):
        super().clean()
        day = self.cleaned_data["day"]
        lesson = self.cleaned_data["lesson"]
        lessons = Lesson.objects.filter(is_saturday=True)
        if day == 'Saturday':
            print(day)
            if not lesson in lessons:
                print(lesson)
                raise forms.ValidationError('В субботу нет' + " " + str(lesson.index) + 'й' + " " + "пары" )


    class Meta:
        model = Schedule
        fields = ['day', 'lesson', 'discipline', 'group', 'teacher', 'auditoriya']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Выберите другой день, пару или аудиторию",

            }
        }


class FullSearchForm(forms.Form):
    start_date = forms.DateField(label='введите дату начала', widget=DatePickerInput(format='%d/%m/%Y'))
    end_date = forms.DateField(label='введите дату окончания', widget=DatePickerInput(format='%d/%m/%Y'))
    discipline = forms.ModelChoiceField(required=False, queryset=Discipline.objects.all(), label="По дисциплине",  widget=forms.Select
                           (attrs={'class':'form-control'}))



class DisciplineForm(forms.ModelForm):
    teacher = forms.ModelMultipleChoiceField(queryset=User.objects.filter(profile__role__name__contains='Преподаватель'), label='Преподаватель')

    class Meta:
        model = Discipline
        fields = ['name', 'teacher']


class JournalNoteForm(forms.ModelForm):
    class Meta:
        model= JournalNote
        fields = ['theme']


class GradeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grade'].empty_label = None


    class Meta:
        model = JournalGrade
        fields = ['grade', 'description']


class JournalSelectForm(forms.ModelForm):

    class Meta:
        model = GroupJournal
        fields = ['study_group', 'discipline']
