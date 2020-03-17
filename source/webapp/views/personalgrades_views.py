# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404
# from django.views.generic import DetailView
#
# from accounts.models import Family
# from webapp.forms import FullSearchForm
#
#
# class PersonalGradesDetailView(DetailView):
#     template_name = 'personalgrades/personalgrades.html'
#     model = Journal
#     ordering = ['discipline']
#
#
#     def get(self, request, *args, **kwargs):
#         self.form = self.get_search_form()
#         return super().get(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super(PersonalGradesDetailView, self).get_context_data(**kwargs)
#         pk = self.kwargs.get('pk')
#         student = get_object_or_404(User, pk=pk)
#         student_marks = self.get_search_query()
#         context['form'] = self.form     # добавляю поиск
#         context.update({
#             'student': student,
#             'profiles': student_marks,
#             'family_users': Family.objects.filter(family_user=self.request.user),
#         })
#         return context
#
#     def get_search_query(self):
#         pk = self.kwargs.get('pk')
#         if self.form.is_valid():
#             start_date = self.form.cleaned_data['start_date']
#             end_date = self.form.cleaned_data['end_date']
#             discipline = self.form.cleaned_data['discipline']
#             if self.form.cleaned_data['discipline'] == None:
#                 return Journal.objects.filter(student=pk, date__range=(start_date, end_date))
#             else:
#                 return Journal.objects.filter(student=pk, date__range=(start_date, end_date),
#                                             discipline=discipline)
#         else:
#             return Journal.objects.filter(student=pk)
#
#     def get_search_form(self):
#         return FullSearchForm(self.request.GET)
#
