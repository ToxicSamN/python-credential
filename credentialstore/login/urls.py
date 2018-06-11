# /auth/urls.py

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
#from django.contrib.auth.views import login
from .views import public, private, aboutpage, homepage, login

urlpatterns = {
    url(r'^public/', public, name="public"),
    url(r'^private/', private, name="private"),
    url(r'^login/$', login.as_view(), name="login"),
    url(r'^$', homepage.as_view(), name="home"),
    url(r'^about/$', aboutpage.as_view(), name="about"),
}

urlpatterns = format_suffix_patterns(urlpatterns)

