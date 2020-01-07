from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views.views import register_view
from accounts.views.admin_position import AdminPositionCreateView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', register_view, name='create'),
    path('add_admin_position/', AdminPositionCreateView.as_view(), name='add_admin_position')

]
