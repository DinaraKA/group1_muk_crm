from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import DetailView, UpdateView
from .models import User, Profile, Passport
from .forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory



def login_view(request, *args, **kwargs):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url:
                return redirect(next_url)
            return redirect('webapp:index')
        else:
            context['has_error'] = True
            context['next'] = next_url
            context['username'] = username
    else:
        context = {'next': request.GET.get('next')}
    return render(request, 'registration/login.html', context=context)


def logout_view(request, *args, **kwargs):
    logout(request)
    return redirect('webapp:index')


def register_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('webapp:index')
    else:
        form = UserCreationForm()
    return render(request, 'user_create.html', context={'form': form})


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'


class UserPersonalInfoChangeView(UpdateView):
    model = User
    template_name = 'user_info_change.html'
    form_class = UserChangeForm
    context_object_name = 'user_obj'

    def test_func(self):
        return self.request.user.pk == self.kwargs['pk']

    def get_success_url(self):
        return reverse('accounts:detail', kwargs={'pk': self.object.pk})


class UserPasswordChangeView(UpdateView):
    model = User
    template_name = 'user_password_change.html'
    form_class = PasswordChangeForm
    context_object_name = 'user_obj'

    def test_func(self):
        return self.request.user.pk == self.kwargs['pk']

    def get_success_url(self):
        return reverse('accounts:login')


class PassportInline(InlineFormSetFactory):
    model = Passport
    fields = ['series', 'issued_by', 'issued_date', 'address', 'inn', 'nationality', 'sex', 'birth_date']


class ProfileInline(InlineFormSetFactory):
    model = Profile
    fields = ['patronymic', 'phone_number', 'photo', 'address_fact']


class CreateOrderView(CreateWithInlinesView):
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'email']
    inlines = [PassportInline, ProfileInline]
    template_name = 'User_Passport_Profile.html'