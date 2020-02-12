from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views.status_views import StatusListView, StatusCreateView, StatusUpdateView, StatusDeleteView
from accounts.views.user_views import register_view, UserPersonalInfoChangeView, UserPasswordChangeView, UserDetailView, \
    UserSearchView, SearchResultsView, UserDeleteView, StudentListView, UserListView
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
    path('user_create/', register_view, name='user_create'),
    path('user_detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('user_update/<int:pk>/', UserPersonalInfoChangeView.as_view(), name='user_update'),
    path('user_password_change/<int:pk>/', UserPasswordChangeView.as_view(), name='password_change'),
    path('user_delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('user/search/', UserSearchView.as_view(), name='user_search'),
    path('user/search/results/', SearchResultsView.as_view(), name='search_results'),
    path('user/student/<str:status>/', StudentListView.as_view(), name='student_list'),
    path('adminpositions/', AdminPositionIndexView.as_view(), name='adminpositions'),
    path('adminposition/add/', AdminPositionCreateView.as_view(), name='add_admin_position'),
    path('adminposition/change/<int:pk>/', AdminPositionUpdateView.as_view(), name='change_admin_position'),
    path('adminposition/delete/<int:pk>/', AdminPositionDeleteView.as_view(), name='delete_admin_position'),
    path('roles/', RoleIndexView.as_view(), name='roles_list'),
    path('roles/add/', RoleCreateView.as_view(), name='role_add'),
    path('roles/change/<int:pk>/', RoleUpdateView.as_view(), name='role_change'),
    path('roles/delete/<int:pk>/', RoleDeleteView.as_view(), name='role_delete'),
    path('statuses/', StatusListView.as_view(), name='statuses'),
    path('statuses/add/', StatusCreateView.as_view(), name='add_status'),
    path('status/change/<int:pk>/', StatusUpdateView.as_view(), name='change_status'),
    path('status/delete/<int:pk>/', StatusDeleteView.as_view(), name='delete_status'),
    path('social_statuses/', SocialStatusListView.as_view(), name='all_social_statuses'),
    path('social_statuses/add/', SocialStatusCreateView.as_view(), name='add_social_status'),
    path('social_status/change/<int:pk>/', SocialStatusUpdateView.as_view(), name='change_social_status'),
    path('social_status/delete/<int:pk>/', SocialStatusDeleteView.as_view(), name='delete_social_status'),
    path('groups/', GroupListView.as_view(), name='groups'),
    path('group_detail/<int:pk>/', GroupDetailView.as_view(), name='detail_group'),
    path('group/add/', GroupCreateView.as_view(), name='add_group'),
    path('group/change/<int:pk>/', GroupUpdateView.as_view(), name='change_group'),
    path('group/delete/<int:pk>/', GroupDeleteView.as_view(), name='delete_group'),
]

