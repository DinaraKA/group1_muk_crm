from django.contrib.auth.models import User
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
        # if not profile.avatar:
        #     profile.avatar = None
        if commit:
            passport.save()

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'first_name', 'last_name', 'email']
        profile_fields = ['address_fact', 'passport']
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
