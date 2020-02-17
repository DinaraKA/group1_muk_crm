from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import UpdateView, DetailView, ListView, DeleteView, FormView
from accounts.forms import UserCreationForm, UserChangeForm, FullSearchForm
from accounts.models import Passport, Profile, Role, Status
from accounts.forms import UserCreationForm, PasswordChangeForm
from django.shortcuts import redirect, get_object_or_404
from django.utils.http import urlencode
from django.db.models import Q



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
            profile.save()
            role = form.cleaned_data['role']
            profile.save()
            profile.role.set(role)
            login(request, user)
            return HttpResponseRedirect(reverse('accounts:detail', kwargs={"pk": user.pk}))
    else:
        form = UserCreationForm()
    return render(request, 'user_create.html', context={'form': form})


class UserPersonalInfoChangeView(PermissionRequiredMixin, UpdateView):
    model = User
    template_name = 'user_info_change.html'
    form_class = UserChangeForm
    context_object_name = 'user_obj'
    permission_required = "webapp.change_user"
    permission_denied_message = "Доступ запрещен"

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
        # roles = Role.objects.filter(pk=role.pk)
        profile.status = form.cleaned_data['status']
        profile.admin_position = form.cleaned_data['admin_position']
        profile.social_status = form.cleaned_data['social_status']
        passport.save()
        profile.role.set(roles)
        profile.save()
        user.save()
        return self.get_success_url()

    def test_func(self):
        return self.request.user.pk == self.kwargs['pk']

    def get_success_url(self):
        # return HttpResponseRedirect(reverse('accounts:user_detail', kwargs={"pk": self.object.pk}))
        return redirect('accounts:user_detail', pk=self.object.pk)


class UserPasswordChangeView(PermissionRequiredMixin, UpdateView):
    model = User
    template_name = 'user_password_change.html'
    form_class = PasswordChangeForm
    context_object_name = 'user_obj'
    permission_required = "webapp.change_user"
    permission_denied_message = "Доступ запрещен"

    def test_func(self):
        return self.request.user.pk == self.kwargs['pk']

    def get_success_url(self):
        return reverse('accounts:detail', kwargs={"pk": self.object.pk})


class UserDetailView(PermissionRequiredMixin, DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'
    permission_required = "webapp.view_user"
    permission_denied_message = "Доступ запрещен"


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'user'
    permission_required = "webapp.view_user"
    permission_denied_message = "Доступ запрещен"


class UserDeleteView(PermissionRequiredMixin, DeleteView):
    model = User
    template_name = 'user_delete.html'
    success_url = reverse_lazy('webapp:index')
    context_object_name = 'user'
    permission_required = 'accounts.delete_user'
    permission_denied_message = '403 Доступ запрещён!'

    def delete(self, request, *args, **kwargs):
        user = self.object = self.get_object()
        rol = get_object_or_404(Role, name='Студент')
        my = list(user.profile.role.all())
        print(my)
        if rol not in my:
            user.profile.status=get_object_or_404(Status, name='Уволен')
        else:
            user.profile.status = get_object_or_404(Status, name='Отчислен')
        user.profile.save()
        return HttpResponseRedirect(self.get_success_url())


class UserSearchView(FormView):
    template_name = 'search.html'
    form_class = FullSearchForm

    def form_valid(self, form):
        query = urlencode(form.cleaned_data)
        url = reverse('accounts:search_results') + '?' + query
        return redirect(url)


class SearchResultsView(PermissionRequiredMixin, ListView):
    # model = User
    model = Profile
    template_name = 'search.html'
    context_object_name = 'object_list'
    paginate_by = 5
    paginate_orphans = 2
    permission_required = "webapp.view_profile"
    permission_denied_message = "Доступ запрещен"

    def get_queryset(self):
        queryset = super().get_queryset()
        form = FullSearchForm(data=self.request.GET)
        if form.is_valid():
            query = self.get_search_query(form)
            queryset = queryset.filter(query).distinct()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        form = FullSearchForm(data=self.request.GET)
        query = self.get_query_string()
        print(query, 'STRING')
        return super().get_context_data(
            form=form, query=query, object_list=object_list, **kwargs
        )

    def get_query_string(self):
        data = {}
        for key in self.request.GET:
            if key != 'page':
                data[key] = self.request.GET.get(key)
                print(urlencode(data), "DATA")
        return urlencode(data)

    # def get_user_query(self, form):
    #     query = Q()
    #     user = form.cleaned_data.get('user')
    #     if user:
    #         user = form.cleaned_data.get('user')
    #         if user:
    #             query = query | Q(user__username__iexact=user)
    #         comment_author = form.cleaned_data.get('comment_author')
    #         if comment_author:
    #             query = query | Q(comments__user__username__iexact=user)
    #     return query

    def get_search_query(self, form):
        query = Q()
        text = form.cleaned_data.get('text').capitalize()
        if text:
            in_username = form.cleaned_data.get('in_username')
            if in_username:
                query = query | Q(user__username__icontains=text)
            in_first_name = form.cleaned_data.get('in_first_name')
            if in_first_name:
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
            # if in_first_name:
                # query = query | Q(first_name__icontains=text)
            # in_tags = form.cleaned_data.get('in_tags')
            # if in_first_name:
            #     query = query | Q(first_name__iexact=user)
            # in_comment_text = form.cleaned_data.get('in_comment_text')
            # if in_comment_text:
            #     query = query | Q(comments__text__icontains=user)
        # if text==None:
        #     in_username = form.cleaned_data.get('in_username')
        #     if in_username:
        #         # query = query | Q(user__username__icontains=text)
        #         query = query
        #         print(query)
        return query


class StudentListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'user'
    permission_required = "webapp.view_user"
    permission_denied_message = "Доступ запрещен"

    def get_queryset(self):
        status = self.kwargs.get('status')
        users = User.objects.filter(profile__status__name__contains=status)
        print(users)
        return users
