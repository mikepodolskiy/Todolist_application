from django.urls import path

from core.views import UserCreateView, UserLoginView, ProfileView, UpdatePasswordView

urlpatterns = [
    path('signup', UserCreateView.as_view(), name='signup'),
    path('login', UserLoginView.as_view(), name='login'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('update_password', UpdatePasswordView.as_view(), name='password update'),

]
