from . import views
from django.conf.urls import url

app_name = 'feed'
urlpatterns = [
    url('userfeed/', views.CreatePostView.as_view(), name='userfeed'),
    url('post/(?P<pk>\d+)$', views.PostDetailView.as_view(), name='post_detail'),
]
