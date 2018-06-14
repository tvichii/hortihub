from . import views
from django.conf.urls import url

app_name = 'feed'
urlpatterns = [
    url('userfeed/', views.UserFeedView.as_view(), name='userfeed'),
]