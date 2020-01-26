from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views.status_views import StatusListView, StatusCreateView, StatusUpdateView, StatusDeleteView
from accounts.views.user_views import register_view, UserPersonalInfoChangeView, UserPasswordChangeView, UserDetailView
from accounts.views.social_status_views import SocialStatusListView, SocialStatusCreateView, SocialStatusUpdateView, \
    SocialStatusDeleteView
from accounts.views.admin_position_views import AdminPositionIndexView, AdminPositionCreateView, AdminPositionUpdateView, \
    AdminPositionDeleteView
from accounts.views.role_views import RoleIndexView, RoleCreateView, RoleUpdateView, RoleDeleteView
from accounts.views.group_views import GroupListView, GroupDetailView, GroupCreateView, GroupUpdateView, \
    GroupDeleteView
from accounts.views.theme_views import ThemeListView, ThemeCreateView, ThemeUpdateView, ThemeDeleteView
from accounts.views.progress_views import ProgressIndexView, ProgressCreateView, ProgressUpdateView, ProgressDeleteView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('positions/', AdminPositionIndexView.as_view(), name='positions'),
    path('create/', register_view, name='create'),
    path('add_admin_position/', AdminPositionCreateView.as_view(), name='add_admin_position'),
    path('change_admin_position/<int:pk>/', AdminPositionUpdateView.as_view(), name='change_admin_position'),
    path('delete_admin_position/<int:pk>/', AdminPositionDeleteView.as_view(), name='delete_admin_position'),
    path('roles/', RoleIndexView.as_view(), name='roles_list' ),
    path('roles/add/', RoleCreateView.as_view(), name='role_add'),
    path('roles/change/<int:pk>', RoleUpdateView.as_view(), name='role_change'),
    path('roles/delete/<int:pk>', RoleDeleteView.as_view(), name='role_delete'),
    path('all_social_statuses/', SocialStatusListView.as_view(), name='all_social_statuses'),
    path('add_social_statuses/', SocialStatusCreateView.as_view(), name='add_social_status'),
    path('change_social_status/<int:pk>/', SocialStatusUpdateView.as_view(), name='change_social_status'),
    path('delete_social_status/<int:pk>/', SocialStatusDeleteView.as_view(), name='delete_social_status'),
    path('delete_admin_position/<int:pk>/', AdminPositionDeleteView.as_view(), name='delete_admin_position'),
    path('<int:pk>/update', UserPersonalInfoChangeView.as_view(), name='update'),
    path('<int:pk>/password_change', UserPasswordChangeView.as_view(), name='password_change'),
    path('<int:pk>/', UserDetailView.as_view(), name='detail'),
    path('statuses/', StatusListView.as_view(), name='statuses'),
    path('add_statuses/', StatusCreateView.as_view(), name='add_status'),
    path('change_status/<int:pk>/', StatusUpdateView.as_view(), name='change_status'),
    path('delete_status/<int:pk>/', StatusDeleteView.as_view(), name='delete_status'),
    path('groups/', GroupListView.as_view(), name='groups'),
    path('detail_group/<int:pk>/', GroupDetailView.as_view(), name='detail_group'),
    path('add_group/', GroupCreateView.as_view(), name='add_group'),
    path('change_group/<int:pk>/', GroupUpdateView.as_view(), name='change_group'),
    path('delete_group/<int:pk>/', GroupDeleteView.as_view(), name='delete_group'),
    path('themes/', ThemeListView.as_view(), name='themes'),
    path('add_theme/', ThemeCreateView.as_view(), name='add_theme'),
    path('change_theme/<int:pk>/', ThemeUpdateView.as_view(), name='change_theme'),
    path('delete_theme/<int:pk>/', ThemeDeleteView.as_view(), name='delete_theme'),
    path('progress/', ProgressIndexView.as_view(), name='progress'),
    path('add_progress/', ProgressCreateView.as_view(), name='add_progress'),
    path('change_progress/<int:pk>/', ProgressUpdateView.as_view(), name='change_progress'),
    path('delete_progress/<int:pk>/', ProgressDeleteView.as_view(), name='delete_progresse'),
]
