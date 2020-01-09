from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register_view, UserDetailView, UserPersonalInfoChangeView, UserPasswordChangeView, CreateOrderView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', register_view, name='create'),
    path('<int:pk>/', UserDetailView.as_view(), name='detail'),
    path('<int:pk>/update', UserPersonalInfoChangeView.as_view(), name='update'),
    path('<int:pk>/password_change', UserPasswordChangeView.as_view(), name='password_change'),
    path('createall/', CreateOrderView.as_view(), name='create_all')

]
