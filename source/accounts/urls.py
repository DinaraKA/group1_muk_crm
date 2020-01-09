from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views.reg_log_in_out import register_view
from accounts.views.admin_position import AdminPositionIndexView, AdminPositionCreateView, AdminPositionUpdateView, AdminPositionDeleteView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('positions/', AdminPositionIndexView.as_view(), name='positions'),
    path('create/', register_view, name='create'),
    path('add_admin_position/', AdminPositionCreateView.as_view(), name='add_admin_position'),
    path('change_admin_position/<int:pk>/', AdminPositionUpdateView.as_view(), name='change_admin_position'),
    path('delete_admin_position/<int:pk>/', AdminPositionDeleteView.as_view(), name='delete_admin_position')
]
