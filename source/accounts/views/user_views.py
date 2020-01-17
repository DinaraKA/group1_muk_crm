from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import UpdateView, DetailView
from accounts.forms import UserCreationForm, UserChangeForm
from accounts.models import Passport, Profile, Role
from accounts.forms import UserCreationForm, PasswordChangeForm
from django.shortcuts import redirect, get_object_or_404


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
            user.save()
            passport = Passport(
                user=user,
                series=form.cleaned_data['series'],
                issued_by=form.cleaned_data['issued_by'],
                issued_date=form.cleaned_data['issued_date'],
                address=form.cleaned_data['address'],
                inn=form.cleaned_data['inn'],
                nationality=form.cleaned_data['nationality'],
                sex=form.cleaned_data['sex'],
                birth_date=form.cleaned_data['birth_date']
            )
            try:
                photo = request.FILES['photo']
            except:
                photo = None

            profile = Profile(
                user=user,
                # role=form.cleaned_data['role'],
                patronymic=form.cleaned_data['patronymic'],
                phone_number=form.cleaned_data['phone_number'],
                address_fact=form.cleaned_data['address_fact'],
                photo=photo,
            )
            user.set_password(form.cleaned_data['password'])
            passport.save()
            profile.save()
            role = form.cleaned_data['role']
            roles = Role.objects.filter(pk=role.pk)
            profile.save()
            profile.role.set(roles)
            login(request, user)
            return redirect('webapp:index')
    else:
        form = UserCreationForm()
    return render(request, 'user_create.html', context={'form': form})


class UserPersonalInfoChangeView(UpdateView):
    model = User
    template_name = 'user_info_change.html'
    form_class = UserChangeForm
    context_object_name = 'user_obj'

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        user = get_object_or_404(User, id=pk)
        print(user)
        profile = get_object_or_404(Profile, user=pk)
        user = get_object_or_404(User, pk=pk)
        print('yes')
        profile.save()
        role = form.cleaned_data['role']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        series = form.cleaned_data['series']
        issued_by = form.cleaned_data['issued_by']
        issued_date = form.cleaned_data['issued_date']
        address = form.cleaned_data['address']
        inn = form.cleaned_data['inn']
        nationality = form.cleaned_data['nationality']
        patronymic = form.cleaned_data['patronymic']
        phone_number = form.cleaned_data['phone_number']
        address_fact = form.cleaned_data['address_fact']
        photo = form.cleaned_data['photo']
        roles = Role.objects.filter(pk=role.pk)
        profile.save()
        profile.role.set(roles)
        User.objects.update(first_name=first_name, last_name=last_name)
        Passport.objects.update(series=series, issued_by=issued_by, issued_date=issued_date, address=address, inn=inn,
                                nationality=nationality)
        Profile.objects.update(patronymic=patronymic, phone_number=phone_number, address_fact=address_fact,
                               photo=photo)
        return redirect('webapp:index')


    def test_func(self):
        return self.request.user.pk == self.kwargs['pk']

    def get_success_url(self):
        return reverse('webapp:index')


class UserPasswordChangeView(UpdateView):
    model = User
    template_name = 'user_password_change.html'
    form_class = PasswordChangeForm
    context_object_name = 'user_obj'

    def test_func(self):
        return self.request.user.pk == self.kwargs['pk']

    def get_success_url(self):
        return reverse('accounts:login')


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'