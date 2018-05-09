# api/urls.py

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ClientListView, ClientCreateView

urlpatterns = {
    url(r'^clientlist$', ClientListView.as_view(), name="list"),
    url(r'^clientcreate$', ClientCreateView.as_view(), name="create"),
}

urlpatterns = format_suffix_patterns(urlpatterns)