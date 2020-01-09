from django.urls import path
from .views import IndexView, Department1View, Department2View, Department3View
from .views import NewsDetailView, NewsView, NewsAddView, NewsEditView, NewsDeleteView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('departments/department1/', Department1View.as_view(),  name='department1'),
    path('departments/department2/', Department2View.as_view(),  name='department2'),
    path('departments/department3/', Department3View.as_view(),  name='department3'),
    path('news/', NewsView.as_view(), name='news'),
    path('news/<int:pk>', NewsDetailView.as_view(), name='news_detail'),
    path('news/add/', NewsAddView.as_view(), name='news_add'),
    path('news/<int:pk>/edit/', NewsEditView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),

]