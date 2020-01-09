from django.urls import path

from .views import AnnouncementsView, AnnounceDetailView, AnnouncementCreateView, AnnouncementUpdateView, AnnouncementDeleteView
from .views import IndexView, Department1View, Department2View, Department3View
from .views import NewsDetailView, NewsView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('departments/department1/', Department1View.as_view(),  name='department1'),
    path('departments/department2/', Department2View.as_view(),  name='department2'),
    path('departments/department3/', Department3View.as_view(),  name='department3'),
    path('news/', NewsView.as_view(), name='news'),
    path('news/<int:pk>', NewsDetailView.as_view(), name='new_detail'),


    path('announcements/', AnnouncementsView.as_view(), name='announcements'),
    path('announcements/<int:pk>/', AnnounceDetailView.as_view(), name='announce_detail'),
    path('announcements/add/', AnnouncementCreateView.as_view(), name='announce_create'),
    path('announcements/change/<int:pk>/', AnnouncementUpdateView.as_view(), name='announce_change'),
    path('announcements/delete/<int:pk>/', AnnouncementDeleteView.as_view(), name='announce_delete'),
]