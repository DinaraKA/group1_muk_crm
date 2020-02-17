from accounts.models import Role
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.shortcuts import render

class RoleIndexView(ListView):
    template_name = 'role/roles.html'
    model = Role
    context_object_name = 'roles'
    # paginate_by = 4
    # paginate_orphans = 0
    # page_kwarg = 'page'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class RoleCreateView(CreateView):
    model = Role
    template_name = 'add.html'
    fields = ['name']

    def form_valid(self, form):
        text = form.cleaned_data['name']
        if Role.objects.filter(name=text.capitalize()):
            print(text)
            messages.error(self.request, 'Объект с таким названием уже существует!')
            return render(self.request, 'add.html', {})
        else:
            role = Role(name=text.capitalize())
            role.save()
        return self.get_success_url()

    def get_success_url(self):
        return redirect('accounts:roles_list')


class RoleUpdateView(UpdateView):
    model = Role
    template_name = 'change.html'
    fields = ['name']

    def form_valid(self, form):
        text = form.cleaned_data['name']
        if Role.objects.filter(name=text.capitalize()):
            print(text, 'tEXT')
            messages.error(self.request, 'Объект с таким названием уже существует!')
            return render(self.request, 'change.html', {})
        else:
            pk = self.kwargs.get('pk')
            role = get_object_or_404(Role, id=pk)
            print(role, "ROLE")
            print(pk, "PK")
            role.name = text.capitalize()
            # role.name.set(pk)
            role.save()
            # role.save(update_fields=['name'])
        return self.get_success_url()

    def get_success_url(self):
        return redirect('accounts:roles_list')
    # def get_success_url(self):
    #     return redirect('accounts:roles_list')


class RoleDeleteView(DeleteView):
    model = Role
    template_name = 'delete.html'
    success_url = reverse_lazy('accounts:roles_list')
