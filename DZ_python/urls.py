"""DZ_python URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from dj_DZ_python.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^sign_in/$', sign_in, name='sign_in'),
    url(r'^sign_up/$', sign_up, name='sign_up'),
    url(r'^logout/$', log_out, name='logout'),
    url(r'^$',MatchListView.as_view(), name='MatchModel'),
    url(r'^match/(?P<id>\d+)', MatchView.as_view(), name='match_url'),
    url(r'^create_team/$', create_team_view, name='create_team'),
    url(r'^create_match/(?P<type>\w+)$', create_match_view, name='create_match'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
