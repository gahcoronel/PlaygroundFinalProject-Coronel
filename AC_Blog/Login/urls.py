# from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth.views import LogoutView

from Login import views


urlpatterns = [
    path('', views.login_home, name='Login'),
    path('login_request', views.login_request, name='Login_Request'),
    path('register', views.register, name='Register'),
    path('logout', LogoutView.as_view(template_name='Login/logout.html'), name="Logout"),
    path('edit_profile', views.edit_profile, name="Edit_Profile"),
    path('change_password', views.change_password.as_view(), name="Change_Password"),
    path('detail_profile', views.detail_profile, name='Detail_Profile'),
]

