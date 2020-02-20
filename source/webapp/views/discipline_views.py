from webapp.models import Discipline
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.shortcuts import render


class DisciplineListView(ListView):
    template_name = 'disciplines/disciplines.html'
    model = Discipline
    ordering = ["name"]
    context_object_name = 'disciplines'
    paginate_by = 8
    paginate_orphans = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class DisciplineCreateView(CreateView):
    model = Discipline
    template_name = 'add.html'
    fields = ['name', 'teacher']

    def form_valid(self, form):
        text = form.cleaned_data['name']
        teacher_text = form.cleaned_data['teacher']
        if Discipline.objects.filter(name=text.capitalize()):
            messages.error(self.request, 'Объект с таким названием уже существует!')
            return render(self.request, 'add.html', {})
        else:
            discipline = Discipline(name=text.capitalize())
            discipline.save()
            return self.get_success_url()
        # # teacher = teacher_text.teacher()
        # # print(i.last_name, "THIS IS I")
        # print(Discipline.objects.filter(name='Тест'), 'THIS IS DISCIPLINE FILTER')
        # obj, boolean = Discipline.objects.get_or_create(name=text)
        #
        # if boolean == False:
        #     messages.error(self.request, 'Объект с таким названием уже существует!')
        #     return render(self.request, 'add.html', {})
        # else:
        #     dis = Discipline.objects.get(name=text)
        #     for i in teacher_text:
        #         if i in dis.teacher.all():
        #             print("false")
        #         else:
        #             print("true")
        #             obj.teacher.add(i)
        #     obj.save()
        # return self.get_success_url()

    def get_success_url(self):
        return redirect('webapp:disciplines')


class DisciplineUpdateView(UpdateView):
    model = Discipline
    template_name = 'change.html'
    fields = ['name', 'teacher']

    # def form_valid(self, form):
    #     text = form.cleaned_data['name']
    #     teacher_text = form.cleaned_data['teacher']
    #     if Discipline.objects.filter(name=text.capitalize()):
    #         messages.error(self.request, 'Объект с таким названием уже существует!')
    #         return render(self.request, 'add.html', {})
    #     else:
    #         discipline = Discipline(name=text.capitalize())
    #         discipline.save()
    #         return self.get_success_url()

    def get_success_url(self):
        return reverse('webapp:disciplines')


class DisciplineDeleteView(DeleteView):
    model = Discipline
    template_name = 'delete.html'
    success_url = reverse_lazy('webapp:disciplines')

