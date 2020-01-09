from django.contrib.auth.models import User
from django import forms
from .models import Profile


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, strip=False)

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

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'first_name', 'last_name', 'email']


class UserChangeForm(forms.ModelForm):
    patronymic = forms.CharField(label='Отчество', max_length=30, required=False)
    phone_number = forms.CharField(label="Номер телефона", required=False)
    photo = forms.ImageField(label='Фото', required=False)
    address_fact = forms.CharField(max_length=100, label='Фактический Адрес')
    parent_one = forms.ModelMultipleChoiceField(queryset=User.objects.all(), label='Родитель Один', required=False)
    parent_two = forms.ModelMultipleChoiceField(queryset=User.objects.all(), label='Родитель Два', required=False)

    def get_initial_for_field(self, field, field_name):
        if field_name in self.Meta.profile_fields:
            try:
                return getattr(self.instance.profile, field_name)
            except Profile.DoesNotExist:
                return None
        return super().get_initial_for_field(field, field_name)

    def save(self, commit=True):
        user = super().save(commit)
        self.save_profile(commit)
        return user

    def save_profile(self, commit=True):
        try:
            profile = self.instance.profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=self.instance)
        # for field in self.Meta.profile_fields:
        #     setattr(profile, field, self.cleaned_data[field])
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        patronymic = self.cleaned_data['patronymic']
        phone_number = self.cleaned_data.get('phone_number ')
        photo = self.cleaned_data.get('photo')
        address_fact = self.cleaned_data.get('address_fact')
        parent_one = self.cleaned_data.get('parent_one')
        parent_two = self.cleaned_data.get('parent_two')
        # parent_one = User.objects.get(active=True)
        # parent_two = User.objects.get(active=True)
        if not profile.photo:
            profile.photo = None
        if commit:
            profile.save()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'patronymic', 'phone_number', 'photo', 'address_fact', "parent_one", "parent_two"]
        profile_fields = ['patronymic', 'phone_number', 'photo', 'address_fact', "parent_one", "parent_two"]
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email'}


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
