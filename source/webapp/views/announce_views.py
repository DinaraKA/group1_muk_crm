from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from webapp.models import Announcements


class AnnouncementsView(ListView):
    model = Announcements
    template_name = 'announcements/announcements.html'
    context_object_name = 'announcements'
    ordering = ['-created_at']
    paginate_by = 2
    paginate_orphans = 0


class AnnounceDetailView(DetailView):
    model = Announcements
    template_name = 'announcements/announce_detail.html'
    context_object_name = 'announcement'


class AnnouncementCreateView(CreateView):
    model = Announcements
    template_name = 'add.html'
    fields = ['title', 'text', 'photo']

    def get_success_url(self):
        return reverse('webapp:announcements')


class AnnouncementUpdateView(UpdateView):
    model = Announcements
    template_name = 'change.html'
    fields = ['title', 'text', 'photo']
    context_object_name = 'announcement'

    def get_success_url(self):
        return reverse('webapp:announce_detail')


# class AnnouncementDeleteView(DeleteView):
#     model = Announcements
#     template_name = 'delete.html'
#
#     def get_success_url(self):
#         return reverse('webapp:announcements')
