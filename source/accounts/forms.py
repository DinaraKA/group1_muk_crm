from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from accounts.models import AdminPosition
from django import forms
from .models import Profile, Passport, Group, Role, Status, SocialStatus

SEX_CHOICES = (
    ('мужской', 'мужской'),
    ("женский", "женский"),
)


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, strip=False)
    citizenship = forms.CharField(label="Гражданство", initial="Кыргызская Республика")
    series = forms.CharField(label='Пасспорт серия')
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
    social_status=forms.ModelChoiceField(label='Социальный статус', queryset=SocialStatus.objects.all())
    admin_position = forms.ModelChoiceField(label='Должность', queryset=AdminPosition.objects.all(), required=False)

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def get_initial_for_field(self, field, field_name):
        if field_name in self.Meta.profile_fields:
            try:
                return getattr(self.instance.profile, field_name)
            except Profile.DoesNotExist:
                return None
        return super().get_initial_for_field(field, field_name)

    def get_initial_for_passport(self, field, field_name):
        if field_name in self.Meta.profile_fields:
            try:
                return getattr(self.instance.profile, field_name)
            except Passport.DoesNotExist:
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
            profile.save()

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'first_name', 'last_name', 'email']
        profile_fields = ['patronymic', 'phone_number', 'address_fact', 'photo', 'role', 'status', 'admin_position',
                          'social_status']
        passport_fields = ['citizenship', 'series', 'issued_by', 'issued_date', 'address', 'inn', 'nationality',
                           'sex', 'birth_date']


class UserChangeForm(forms.ModelForm):
    citizenship = forms.CharField(label="Гражданство", initial="Кыргызская Республика")
    series = forms.CharField(label='Пасспорт серия')
    issued_by = forms.CharField(label='Кем выдан')
    issued_date = forms.DateField(label='Дата выдачи')
    address = forms.CharField(label='Адрес')
    inn = forms.CharField(label='ИНН')
    nationality = forms.CharField(label='Национальность')
    sex = forms.ChoiceField(choices=SEX_CHOICES, label='Пол')
    birth_date = forms.DateField(label='Дата Рождения')
    patronymic = forms.CharField(label='Отчество')
    phone_number = forms.IntegerField(label='Номер телефона')
    photo = forms.ImageField(label='Фото', required=False)
    address_fact = forms.CharField(label='Фактический адрес')
    role = forms.ModelChoiceField(label='Роль', queryset=Role.objects.all())
    status = forms.ModelChoiceField(label='Статус', queryset=Status.objects.all())
    admin_position = forms.ModelChoiceField(label='Должность', queryset=AdminPosition.objects.all(), required=False)
    social_status = forms.ModelChoiceField(label='Социальный Статус', queryset=SocialStatus.objects.all(), required=False)


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

    def save(self, commit=True):
        user = super().save(commit=False)
        self.save_passport(commit)
        self.save_profile(commit)
        return user

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
        if commit:
            profile.save()

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
    class Meta:
        model = Group
        fields = ['name', 'students', 'starosta', 'kurator', 'started_at']


class FullSearchForm(forms.Form):
    text = forms.CharField(max_length=100, required=False, label='Поиск')
    in_username = forms.BooleanField(initial=False, required=False, label='По Username')
    in_first_name = forms.BooleanField(initial=True, required=False, label='По имени')
    in_role = forms.BooleanField(initial=False, required=False, label='По роли')
    in_status = forms.BooleanField(initial=False, required=False, label='По статусу')
    in_admin_position = forms.BooleanField(initial=False, required=False, label='По должности')
    in_social_status = forms.BooleanField(initial=False, required=False, label='По соц статусу')

    def clean(self):
        super().clean()
        data = self.cleaned_data
        text = data.get('text')
        # user = data.get('user')
        if not (text):
            raise ValidationError('No search text or author provided',
                                  code='text_and_author_empty')
        errors = []
        if text:
            in_username = data.get('in_username')
            in_first_name = data.get('in_first_name')
            in_role = data.get('in_role')
            in_status = data.get('in_status')
            in_admin_position = data.get('in_admin_position')
            in_social_status = data.get('in_social_status')
            if not (in_username or in_first_name or in_role or in_status or in_admin_position or in_social_status):
                errors.append(ValidationError(
                    'One of the checkboxes should be checked: In title, In text, In tags, In comment text',
                    code='text_search_criteria_empty'
                ))
        if errors:
            raise ValidationError(errors)
        return data