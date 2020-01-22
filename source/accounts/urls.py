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


app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', register_view, name='create'),
    path('<int:pk>/', UserDetailView.as_view(), name='detail'),
    path('password_change/<int:pk>', UserPasswordChangeView.as_view(), name='password_change'),
    path('update/<int:pk>', UserPersonalInfoChangeView.as_view(), name='update'),
    path('admin_position/all/', AdminPositionIndexView.as_view(), name='positions'),
    path('admin_position/add/', AdminPositionCreateView.as_view(), name='add_admin_position'),
    path('admin_position/change/<int:pk>/', AdminPositionUpdateView.as_view(), name='change_admin_position'),
    path('admin_position/delete/<int:pk>/', AdminPositionDeleteView.as_view(), name='delete_admin_position'),
    path('role/all/', RoleIndexView.as_view(), name='roles_list'),
    path('role/add/', RoleCreateView.as_view(), name='role_add'),
    path('role/change/<int:pk>', RoleUpdateView.as_view(), name='role_change'),
    path('role/delete/<int:pk>', RoleDeleteView.as_view(), name='role_delete'),
    path('social_status/all/', SocialStatusListView.as_view(), name='all_social_statuses'),
    path('social_status/add/', SocialStatusCreateView.as_view(), name='add_social_status'),
    path('social_status/change/<int:pk>/', SocialStatusUpdateView.as_view(), name='change_social_status'),
    path('social_status/delete/<int:pk>/', SocialStatusDeleteView.as_view(), name='delete_social_status'),
    path('status/all/', StatusListView.as_view(), name='statuses'),
    path('status/add/', StatusCreateView.as_view(), name='add_status'),
    path('status/change/<int:pk>/', StatusUpdateView.as_view(), name='change_status'),
    path('status/delete/<int:pk>/', StatusDeleteView.as_view(), name='delete_status'),
    path('group/all/', GroupListView.as_view(), name='groups'),
    path('group/detail/<int:pk>/', GroupDetailView.as_view(), name='detail_group'),
    path('group/add/', GroupCreateView.as_view(), name='add_group'),
    path('group/change/<int:pk>/', GroupUpdateView.as_view(), name='change_group'),
    path('group/delete/<int:pk>/', GroupDeleteView.as_view(), name='delete_group'),
]
