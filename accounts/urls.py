from . import views
from django.conf.urls import url

app_name = 'accounts'
urlpatterns = [
    url('signup/', views.SignUp.as_view(), name='signup'),
    url('editprof/(?P<pk>[0-9]+)/', views.UserUpdate.as_view(), name='editprof'),
    url('users/', views.UserListView.as_view(), name='users_list'),
    url('user/follow/(?P<pk>[0-9]+)/', views.UserFollow.as_view(), name='user_follow'),
    url('userdetail/(?P<pk>[0-9]+)/', views.UserDetail.as_view(), name='userdetail'),
]
