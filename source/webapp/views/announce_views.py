from django.views.generic import ListView, DetailView
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