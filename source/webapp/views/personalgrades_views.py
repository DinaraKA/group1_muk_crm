from django.views.generic import ListView

from webapp.models import Journal


class PersonalGradesListView(ListView):
    template_name = 'personalgrades/personalgrades.html'
    model = Journal
    ordering = ["discipline"]
    context_object_name = 'grades'

    def get_context_data(self, **kwargs):
        context = super(PersonalGradesListView, self).get_context_data(**kwargs)
        context.update({
            'grades': Journal.objects.order_by('date')
        })
        return context

