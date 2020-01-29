from django.views.generic import ListView

from accounts.models import Progress


class PersonalGradesListView(ListView):
    template_name = 'personalgrades/personalgrades.html'
    model = Progress
    ordering = ["discipline"]
    context_object_name = 'grades'

    def get_context_data(self, **kwargs):
        context = super(PersonalGradesListView, self).get_context_data(**kwargs)
        context.update({
            'grades': Progress.objects.order_by('date')
        })
        return context

