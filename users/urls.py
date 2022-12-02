from django.urls import path
from .views import LoginUser, LogoutUser, RegisterUser

urlpatterns = [
    path('login', LoginUser.as_view(), name='login_user'),
    path('logout', LogoutUser.as_view(), name='logout_user'),
    path('register', RegisterUser.as_view(), name='register_user')
]
