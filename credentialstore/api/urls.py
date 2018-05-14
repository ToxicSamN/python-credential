# api/urls.py

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ClientListView, ClientCreateView, SecretListView


urlpatterns = {
    url(r'^ListClient$', ClientListView.as_view(), name="list"),
    url(r'^CreateClient$', ClientCreateView.as_view(), name="create"),
    url(r'^GetSecret$', SecretListView.as_view(), name="get_secret"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
