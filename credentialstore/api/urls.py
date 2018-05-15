# api/urls.py

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ClientListView, ClientCreateView, SecretListView, RealClientListView, ClientDetailsView


urlpatterns = {
    url(r'^GetClient$', RealClientListView.as_view(), name="list"),
    # url(r'^client/(?P<ClientId>[0-9a-z]{1,65535})/$', ClientDetailsView.as_view(), name="details"),
    # url(r'^RealListClient$', RealClientListView.as_view(), name="list"),
    url(r'^CreateClient$', ClientCreateView.as_view(), name="create"),
    url(r'^GetSecret$', SecretListView.as_view(), name="get_secret"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
