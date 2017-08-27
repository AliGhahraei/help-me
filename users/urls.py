from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

from . import views


urlpatterns = [
    url('login', auth_views.LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name='login'),
    url('services', views.ServiceList.as_view(), name='service_list')
    url('register', views.signup, name='register'),
]
