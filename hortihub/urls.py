"""hortihub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('admin/', admin.site.urls),
    url('^accounts/', include('accounts.urls', namespace='accounts')),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^feed/', include('feed.urls', namespace='feed')),
    # url(r'^actions/', include('actions.urls', namespace='actions')),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^', include('hortihome.urls',  namespace='hortihome')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, # not for prdocution use, used in debug
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ]
