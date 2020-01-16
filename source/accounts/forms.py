from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from accounts.models import AdminPosition
from django import forms
from .models import Profile, Passport


SEX_CHOICES = (
    ('man', 'мужской'),
    ("women", "женский"),
)


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, strip=False)
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
            # except Profile.DoesNotExist:
                return None
        return super().get_initial_for_field(field, field_name)

    def save_passport(self, commit=True):
        try:
            passport = self.instance.passport
        except Passport.DoesNotExist:
            passport = Passport.objects.create(passport=self.instance)
        for field in self.Meta.passport_fields:
            setattr(passport, field, self.cleaned_data[field])
        # if not profile.avatar:
        #     profile.avatar = None
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
        profile_fields = ['patronymic', 'phone_number', 'address_fact', 'photo']
        passport_fields = ['series', 'issued_by', 'issued_date', 'address', 'inn', 'nationality', 'sex', 'birth_date']


class UserChangeForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, strip=False)
    series = forms.CharField(label='Пасспорт серия')
    issued_by = forms.CharField(label='Кем выдан')
    issued_date = forms.DateField(label='Дата выдачи')
    address = forms.CharField(label='Адрес')
    inn = forms.CharField(label='ИНН')
    nationality = forms.CharField(label='Национальность')
    sex = forms.ChoiceField(choices=SEX_CHOICES, label='Пол')
    birth_date = forms.DateField(label='Дата Рождения')

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        return password_confirm

    def get_initial_for_field(self, field, field_name):
        if field_name in self.Meta.passport_fields:
            try:
                return getattr(self.instance.passport, field_name)
            except Passport.DoesNotExist:
                return None
        return super().get_initial_for_field(field, field_name)

    def save(self, commit=True):
        user = super().save(commit=False)
        self.save_passport(commit)
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

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'first_name', 'last_name', 'email']
        # profile_fields = ['address_fact', 'passport']
        passport_fields = ['series', 'issued_by', 'issued_date', 'address', 'inn', 'nationality', 'sex', 'birth_date']


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
