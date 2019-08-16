# /credentialstore/urls.py

"""credentialstore URL Configuration"""

from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from accounts.forms import LoginForm

urlpatterns = [
    url('admin/login/', LoginView.as_view(template_name='registration/login.html', authentication_form=LoginForm)),
    url('admin/', admin.site.urls, name='admin'),
    url(r'credentialstore/', include('api.urls')),
    url(r'^', include('accounts.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^login/$', LoginView.as_view(template_name='registration/login.html', authentication_form=LoginForm)),
    url(r'^logout/$', LogoutView.as_view(next_page='/accounts/login')),
]


urlpatterns += staticfiles_urlpatterns()
