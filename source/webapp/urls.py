from django.urls import path

from webapp.views import AuditoryListView, AuditoryCreateView, AuditoryUpdateView, AuditoryDeleteView
from .views import AnnouncementsView, AnnounceDetailView, AnnouncementCreateView, AnnouncementUpdateView, AnnouncementDeleteView
from .views import IndexView, Department1View, Department2View, Department3View
from .views import NewsDetailView, NewsView, NewsAddView, NewsEditView, NewsDeleteView
from .views import GradeListView, GradeCreateView, GradeUpdateView, GradeDeleteView
from .views import DisciplineListView, DisciplineCreateView, DisciplineUpdateView, DisciplineDeleteView
from .views import LessonListView, LessonCreateView, LessonUpdateView, LessonDeleteView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('department/department1/', Department1View.as_view(),  name='department1'),
    path('department/department2/', Department2View.as_view(),  name='department2'),
    path('department/department3/', Department3View.as_view(),  name='department3'),
    path('news/all', NewsView.as_view(), name='news'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('news/add/', NewsAddView.as_view(), name='news_add'),
    path('news/change/<int:pk>/', NewsEditView.as_view(), name='news_edit'),
    path('news/delete/<int:pk>/', NewsDeleteView.as_view(), name='news_delete'),
    path('announcements/', AnnouncementsView.as_view(), name='announcements'),
    path('announcements/<int:pk>/', AnnounceDetailView.as_view(), name='announce_detail'),
    path('announcements/add/', AnnouncementCreateView.as_view(), name='announce_create'),
    path('announcements/change/<int:pk>/', AnnouncementUpdateView.as_view(), name='announce_change'),
    path('announcements/delete/<int:pk>/', AnnouncementDeleteView.as_view(), name='announce_delete'),
    path('auditories/', AuditoryListView.as_view(), name='auditories'),
    path('auditories/add/', AuditoryCreateView.as_view(), name='add_auditory'),
    path('auditories/change/<int:pk>/', AuditoryUpdateView.as_view(), name='change_auditory'),
    path('auditories/delete/<int:pk>/', AuditoryDeleteView.as_view(), name='delete_auditory'),
    path('grades/', GradeListView.as_view(), name='grades'),
    path('grades/add/', GradeCreateView.as_view(), name='add_grade'),
    path('grades/change/<int:pk>/', GradeUpdateView.as_view(), name='change_grade'),
    path('grades/delete/<int:pk>/', GradeDeleteView.as_view(), name='delete_grade'),
    path('disciplines/', DisciplineListView.as_view(), name='disciplines'),
    path('disciplines/add/', DisciplineCreateView.as_view(), name='add_discipline'),
    path('disciplines/change/<int:pk>/', DisciplineUpdateView.as_view(), name='change_discipline'),
    path('disciplines/delete/<int:pk>/', DisciplineDeleteView.as_view(), name='delete_discipline'),
    path('lessons/all/', LessonListView.as_view(), name='lessons'),
    path('lessons/add/', LessonCreateView.as_view(), name='lesson_create'),
    path('lessons/update/<int:pk>/', LessonUpdateView.as_view(), name='lesson_update'),
    path('lessons/delete/<int:pk>/', LessonDeleteView.as_view(), name='lesson_delete'),
]