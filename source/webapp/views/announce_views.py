from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.models import Announcements


class AnnouncementsView(ListView):
    model = Announcements
    template_name = 'announcements/announcements.html'
    context_object_name = 'announcements'
    ordering = ['-created_at']
    paginate_by = 10
    paginate_orphans = 0


class AnnounceDetailView(DetailView):
    model = Announcements
    template_name = 'announcements/announce_detail.html'
    context_object_name = 'announcement'


class AnnouncementCreateView(UserPassesTestMixin, CreateView):
    model = Announcements
    template_name = 'add.html'
    fields = ['title', 'text', 'photo']

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

    def get_success_url(self):
        return reverse('webapp:announcements')


class AnnouncementUpdateView(UserPassesTestMixin, UpdateView):
    model = Announcements
    template_name = 'change.html'
    fields = ['title', 'text', 'photo']
    context_object_name = 'announcement'

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

    def get_success_url(self):
        return reverse('webapp:announcements')


class AnnouncementDeleteView(UserPassesTestMixin, DeleteView):
    model = Announcements
    template_name = 'delete.html'

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')

    def get_success_url(self):
        return reverse('webapp:announcements')
