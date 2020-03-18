from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import UpdateView, DetailView, ListView, DeleteView, FormView, CreateView, TemplateView
from accounts.forms import UserCreationForm, UserChangeForm, FullSearchForm, UserFamilyForm, PasswordChangeForm
from accounts.models import Passport, Profile, Role, Status, Family, StudyGroup
from django.shortcuts import redirect, get_object_or_404
from django.utils.http import urlencode
from django.db.models import Q
from ajax_search.forms import SearchForm



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
                citizenship=form.cleaned_data['citizenship'],
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
                patronymic=form.cleaned_data['patronymic'],
                phone_number=form.cleaned_data['phone_number'],
                address_fact=form.cleaned_data['address_fact'],
                photo=photo,
                status=form.cleaned_data['status'],
                admin_position=form.cleaned_data['admin_position'],
                social_status=form.cleaned_data['social_status']
            )
            user.set_password(form.cleaned_data['password'])
            passport.save()
            roles = form.cleaned_data['role']
            profile.save()
            profile.role.set(roles)
            for role in roles:
                if role.name == "Учебная часть":
                    group = Group.objects.get(name='principal_staff')
                    user.groups.add(group)
                elif role.name == "Преподаватель":
                    group = Group.objects.get(name='teachers')
                    user.groups.add(group)
                    user.save()
            return HttpResponseRedirect(reverse('accounts:user_detail', kwargs={"pk": user.pk}))
    else:
        form = UserCreationForm()
    return render(request, 'user_create.html', context={'form': form})


class UserPersonalInfoChangeView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'user_info_change.html'
    form_class = UserChangeForm

    def test_func(self):
        user_requesting = self.request.user
        user_detail = User.objects.get(pk=self.kwargs['pk'])
        return user_requesting.is_staff or user_requesting.groups.filter(name='principal_staff')

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        user = get_object_or_404(User, id=pk)
        passport = get_object_or_404(Passport, user=pk)
        profile = get_object_or_404(Profile, user=pk)
        user = get_object_or_404(User, pk=pk)
        roles = form.cleaned_data['role']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        passport.series = form.cleaned_data['series']
        passport.issued_by = form.cleaned_data['issued_by']
        passport.issued_date = form.cleaned_data['issued_date']
        passport.address = form.cleaned_data['address']
        passport.inn = form.cleaned_data['inn']
        passport.nationality = form.cleaned_data['nationality']
        passport.citizenship = form.cleaned_data['citizenship']
        passport.sex = form.cleaned_data['sex']
        profile.patronymic = form.cleaned_data['patronymic']
        profile.phone_number = form.cleaned_data['phone_number']
        profile.address_fact = form.cleaned_data['address_fact']
        profile.photo = form.cleaned_data['photo']
        profile.status = form.cleaned_data['status']
        profile.admin_position = form.cleaned_data['admin_position']
        profile.social_status = form.cleaned_data['social_status']
        passport.save()
        profile.role.set(roles)
        profile.save()
        user.save()
        return self.get_success_url()

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={"pk": self.object.pk})


class UserPasswordChangeView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'user_password_change.html'
    form_class = PasswordChangeForm
    context_object_name = 'user_obj'

    def test_func(self):
        user_requesting = self.request.user
        user_detail = User.objects.get(pk=self.kwargs['pk'])
        return user_requesting.is_staff or user_requesting.groups.filter(name='principal_staff')

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={"pk": self.object.pk})


class UserDetailView(UserPassesTestMixin, DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'

    def test_func(self):
        user_requesting = self.request.user
        user_detail = User.objects.get(pk=self.kwargs['pk'])
        return user_requesting.is_staff or user_requesting.groups.filter(name='principal_staff') or user_detail == user_requesting

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs['pk'])
        students = Family.objects.filter(family_user=user)
        role_student = User.objects.filter(profile__role__name__icontains='Студент')
        context.update({
            'role_student': role_student,
            'family': Family.objects.filter(student=user),
            'groups': StudyGroup.objects.filter(students__in=students.values('student')),
            'students': students,
            'student_user': User.objects.filter(profile__role__name ='Студент'),
            'parent_user': User.objects.filter(profile__role__name ='Родитель')
        })
        return context


class UserListView(UserPassesTestMixin, ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'user'

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')


class UserDeleteView(UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'user_delete.html'
    success_url = reverse_lazy('webapp:index')
    context_object_name = 'user'

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

    def delete(self, request, *args, **kwargs):
        user = self.object = self.get_object()
        rol = get_object_or_404(Role, name='Студент')
        my = list(user.profile.role.all())
        print(my)
        if rol not in my:
            user.profile.status = get_object_or_404(Status, name='Уволен')
        else:
            user.profile.status = get_object_or_404(Status, name='Отчислен')
        user.profile.save()
        return HttpResponseRedirect(self.get_success_url())


class UserSearchView(FormView):
    template_name = 'search.html'
    form_class = FullSearchForm

    # def test_func(self):
    #     user_requesting = self.request.user
    #     user_detail = User.objects.get(pk=self.kwargs['pk'])
    #     return user_requesting.is_staff or user_requesting.groups.filter(name='principal_staff') or user_detail == user_requesting

    def form_valid(self, form):
        query = urlencode(form.cleaned_data)
        url = reverse('accounts:search_results') + '?' + query
        return redirect(url)


class SearchUser(UserPassesTestMixin, TemplateView):
    template_name = "user_search.html"

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        result_list = []
        q = self.request.GET.get('q', None)
        if q:
            result_list = [user for user in User.objects.filter(
                Q(first_name__icontains=q) | Q(last_name__icontains=q))]
            context = {
                "result": result_list,
                "query": q,
            }
        return context


class SearchResultsView(UserPassesTestMixin, ListView):
    model = Profile
    template_name = 'search.html'
    context_object_name = 'object_list'
    paginate_by = 5
    paginate_orphans = 2

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

    def get_queryset(self):
        queryset = super().get_queryset()
        form = FullSearchForm(data=self.request.GET)
        if form.is_valid():
            query = self.get_search_query(form)
            queryset = queryset.filter(query).distinct()
        return queryset

    def get_context_data(self, *, object_list=None, group_list=None, text=None, user_list=None, **kwargs):
        form = FullSearchForm(data=self.request.GET)
        if form.is_valid():
            text = form.cleaned_data.get("text")
        query = self.get_query_string()
        group_list = StudyGroup.objects.filter(name__icontains=text)
        if not group_list.exists():
            group_list = None
        user_list = User.objects.filter(first_name__icontains=text)
        return super().get_context_data(
            form=form, query=query, object_list=object_list,
            group_list=group_list, user_list=user_list
        )

    def get_query_string(self):
        data = {}
        for key in self.request.GET:
            if key != 'page':
                data[key] = self.request.GET.get(key)
        return urlencode(data)

    def get_search_query(self, form):
        query = Q()
        text = form.cleaned_data.get('text').capitalize()
        if text:
            in_username = form.cleaned_data.get('in_username')
            if in_username:
                query = query | Q(user__username__icontains=text)
            in_first_name = form.cleaned_data.get('in_first_name')
            if in_first_name:
                if "-" in text:
                    first_name, last_name = text.split('-')
                    query = query | Q(user__first_name__icontains=first_name) | Q(user__last_name__icontains=last_name)
                else:
                    query = query | Q(user__first_name__icontains=text)
            in_status = form.cleaned_data.get('in_status')
            if in_status:
                query = query | Q(status__name__icontains=text)
            in_role = form.cleaned_data.get('in_role')
            if in_role:
                query = query | Q(role__name__icontains=text)
            in_admin_position = form.cleaned_data.get('in_admin_position')
            if in_admin_position:
                query = query | Q(admin_position__name__icontains=text)
            in_social_status = form.cleaned_data.get('in_social_status')
            if in_social_status:
                query = query | Q(social_status__name__icontains=text)
        return query


class StudentListView(UserPassesTestMixin, ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'user'

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

    def get_queryset(self):
        status = self.kwargs.get('status')
        users = User.objects.filter(profile__status__name__contains=status)
        print(users)
        return users


class UserFamilyCreateView(UserPassesTestMixin, CreateView):
    template_name = 'user_family_create.html'
    form_class = UserFamilyForm

    def test_func(self):
        user_requesting = self.request.user
        user_detail = User.objects.get(pk=self.kwargs['pk'])
        return user_requesting.is_staff or user_requesting.groups.filter(name='principal_staff')

    def form_valid(self, form):
        self.student_pk = self.kwargs.get('pk')
        student = get_object_or_404(User, pk=self.student_pk)
        user = User(
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email']
        )
        user.set_password(form.cleaned_data['password'])
        user.save()
        profile = Profile(
            user=user,
            phone_number=form.cleaned_data['phone_number']
        )
        profile.save()
        role = Role.objects.get(name='Родитель')
        profile.save()
        profile.role.add(role)
        Family.objects.create(student=student, family_user= user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={"pk": self.student_pk})


class UserFamilyCreate2View(UserPassesTestMixin, CreateView):
    model = Family
    template_name = 'add.html'
    fields = ['family_user']

    def test_func(self):
        user_requesting = self.request.user
        user_detail = User.objects.get(pk=self.kwargs['pk'])
        return user_requesting.is_staff or user_requesting.groups.filter(name='principal_staff')

    def form_valid(self, form):
        self.student_pk = self.kwargs.get('pk')
        student = get_object_or_404(User, pk=self.student_pk)
        family_user = form.cleaned_data['family_user']
        role = Role.objects.get(name='Родитель')
        family_user.profile.role.add(role)
        Family.objects.create(student=student, family_user=family_user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={"pk": self.student_pk})


class FamilyDeleteView(UserPassesTestMixin, DeleteView):
    model = Family
    template_name = 'delete.html'

    def test_func(self):
        user_requesting = self.request.user
        user_detail = User.objects.get(pk=self.kwargs['pk'])
        return user_requesting.is_staff or user_requesting.groups.filter(name='principal_staff')

    def delete(self, request, *args, **kwargs):
        family = self.object = self.get_object()
        parent = Family.objects.filter(family_user=family.family_user)
        family.delete()
        if parent:
            pass
        else:
            family.family_user.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={"pk": self.object.student.pk})

