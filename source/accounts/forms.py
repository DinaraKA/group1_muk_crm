from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from accounts.models import AdminPosition
from django import forms
from .models import Profile, Passport, StudyGroup, Role, Status, SocialStatus

SEX_CHOICES = (
    ('мужской', 'мужской'),
    ("женский", "женский"),
)


class UserForm(forms.ModelForm):
    citizenship = forms.CharField(label="Гражданство", initial="Кыргызская Республика")
    series = forms.CharField(label='Пасспорт серия', initial="jjj")
    issued_by = forms.CharField(label='Кем выдан', required=False)
    issued_date = forms.DateField(label='Дата выдачи')
    address = forms.CharField(label='Адрес')
    inn = forms.CharField(label='ИНН', required=False)
    nationality = forms.CharField(label='Национальность', required=False)
    sex = forms.ChoiceField(choices=SEX_CHOICES, label='Пол')
    birth_date = forms.DateField(label='Дата Рождения')
    patronymic = forms.CharField(label='Отчество', required=False)
    phone_number = forms.IntegerField(label='Номер телефона', required=False)
    photo = forms.ImageField(label='Фото', required=False)
    address_fact = forms.CharField(label='Фактический адрес')
    role = forms.ModelMultipleChoiceField(label='Роль', queryset=Role.objects.all())
    status = forms.ModelChoiceField(label='Статус', queryset=Status.objects.all())
    social_status = forms.ModelChoiceField(label='Социальный статус', queryset=SocialStatus.objects.all(),
                                           required=False)
    admin_position = forms.ModelChoiceField(label='Должность', queryset=AdminPosition.objects.all(), required=False)

    def clean_status(self):
        roles = self.cleaned_data.get("role", '')
        status = self.cleaned_data.get('status')

        if status.name in ["Очная форма обучения", "Заочная форма обучения", "Дистанционная форма обучения"]:
            for role in roles:
                if role.name == "Студент":
                    return status
            raise forms.ValidationError('Статус форма обучения может быть только у студента!')
        if status.name == "Отчислен":
            for role in roles:
                if role.name == "Студент":
                    return status
            raise forms.ValidationError('Отчислен может быть только студент!')
        if status.name == "Уволен":
            for role in roles:
                if role.name in ["Технический работник", "Административный работник", "Преподаватель", "Учебная часть"]:
                    return status
            raise forms.ValidationError('Уволен может быть только работник или преподаватель!')
        if status.name == "Родитель/ Опекун":
            for role in roles:
                if role.name == "Родитель":
                    return status
            raise forms.ValidationError('Статус родитель может иметь только пользователь с ролью родитель/ опекун!')
        if status.name in ["Полная занятость", "Часовая форма работы"]:
            for role in roles:
                if role.name in ["Технический работник", "Административный работник", "Преподаватель", "Учебная часть"]:
                    return status
            raise forms.ValidationError(
                'Полную занятость или часовую форму работы может иметь только работник или преподаватель!')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def get_initial_for_field(self, field, field_name):
        if field_name in self.Meta.passport_fields:
            try:
                return getattr(self.instance.passport, field_name)
            except Passport.DoesNotExist:
                return None

        if field_name in self.Meta.profile_fields:
            try:
                return getattr(self.instance.profile, field_name)
            except Profile.DoesNotExist:
                return None
        return super().get_initial_for_field(field, field_name)

    def save_passport(self, commit=True):
        try:
            passport = self.instance.passport
        except Passport.DoesNotExist:
            passport = Passport.objects.create(passport=self.instance)
        for field in self.Meta.passport_fields:
            setattr(passport, field, self.cleaned_data[field])
        if commit:
            passport.save()

    def save_profile(self, commit=True):
        try:
            profile = self.instance.profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(profile=self.instance)
        for field in self.Meta.profile_fields:
            setattr(profile, field, self.cleaned_data[field])
        if not profile.photo:
            profile.photo = None
        if commit:
            self.check_status()
            profile.save()


class UserCreationForm(UserForm):
    password = forms.CharField(label="Пароль", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, strip=False)

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        return password_confirm

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'first_name', 'last_name', 'email']
        profile_fields = ['patronymic', 'phone_number', 'address_fact', 'photo', 'role', 'status', 'admin_position',
                          'social_status']
        passport_fields = ['citizenship', 'series', 'issued_by', 'issued_date', 'address', 'inn', 'nationality',
                           'sex', 'birth_date']


class UserChangeForm(UserForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        profile_fields = ['patronymic', 'phone_number', 'address_fact', 'photo', 'role', 'status', 'admin_position',
                          'social_status'
                          ]
        passport_fields = ['citizenship', 'series', 'issued_by', 'issued_date', 'address', 'inn', 'nationality', 'sex',
                           'birth_date']


class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(label="Новый пароль", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, strip=False)
    old_password = forms.CharField(label="Старый пароль", strip=False, widget=forms.PasswordInput)

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        return password_confirm

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Старый пароль неправильный!')
        return old_password

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['password', 'password_confirm', 'old_password']


class AdminPositionForm(forms.ModelForm):
    name = forms.CharField()

    def clean_name(self):
        data = self.cleaned_data['name']

        if not data:
            raise ValidationError('This field is required')

    class Meta:
        model = AdminPosition
        fields = ['name']


class GroupForm(forms.ModelForm):
    head_teacher = forms.ModelChoiceField(queryset=User.objects.filter(profile__role__name='Преподаватель'), label='Куратор')

    class Meta:
        model = StudyGroup
        fields = ['name', 'students', 'group_leader', 'head_teacher', 'started_at']


class FullSearchForm(forms.Form):
    text = forms.CharField(max_length=100, required=False, label='Поиск')
    in_username = forms.BooleanField(initial=False, required=False, label='По Username')
    in_first_name = forms.BooleanField(initial=True, required=False, label='По имени')
    in_role = forms.BooleanField(initial=False, required=False, label='По роли')
    in_status = forms.BooleanField(initial=False, required=False, label='По статусу')
    in_admin_position = forms.BooleanField(initial=False, required=False, label='По должности')
    in_social_status = forms.BooleanField(initial=False, required=False, label='По соц статусу')
    in_group = forms.BooleanField(initial=False, required=False, label='По группе')

    def clean(self):
        super().clean()
        data = self.cleaned_data
        text = data.get('text')
        # user = data.get('user')
        if not (text):
            raise ValidationError('Вы не ввели текст поиска!',
                                  code='text_search_empty')
        errors = []
        if text:
            in_username = data.get('in_username')
            in_first_name = data.get('in_first_name')
            in_role = data.get('in_role')
            in_status = data.get('in_status')
            in_admin_position = data.get('in_admin_position')
            in_social_status = data.get('in_social_status')
            in_group = data.get('in_group')
            if not (in_username or in_first_name or in_role or in_status or in_admin_position or in_social_status
                    or in_group):
                errors.append(ValidationError(
                    'Пожулайста отметте критерии поиска, выставите галочки, где необходимо искать',
                    code='text_search_criteria_empty'
                ))
        if errors:
            raise ValidationError(errors)
        return data


class UserFamilyForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    phone_number = forms.CharField(max_length=20, label='Контакты', empty_value=True)
    password = forms.CharField(label="Пароль", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, strip=False)

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        return password_confirm

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'password_confirm', 'email', 'phone_number']

