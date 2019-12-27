from django.urls import path
from .views import IndexView, Department1View, Department2View

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('departments/department1', Department1View.as_view(),  name='department1'),
    path('departments/department2', Department2View.as_view(),  name='department2')
]