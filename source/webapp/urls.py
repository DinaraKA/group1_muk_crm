from django.urls import path
from .views import NewsDetailView, NewsView


app_name = 'webapp'

urlpatterns = [
    # path('', IndexView.as_view(), name='index'),
    path('news/', NewsView.as_view(), name='news'),
    path('news/<int:pk>', NewsDetailView.as_view(), name='new_detail'),


]