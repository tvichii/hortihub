from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'hortihome'

urlpatterns = [
url(r'^$', views.HomeView.as_view(), name='home'),
    # url(r'^$', auth_views.login, name='login'),
]