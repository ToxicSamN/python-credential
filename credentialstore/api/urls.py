# api/urls.py

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import GetCredentialView, AdminGetClientsView, AdminGetClientView, NewClientId
from.frontend_views import CreateClientView, UpdateClientView
from .views import AdminGetSecretsView, AdminGetSecretView, AdminGetSecretClientsView
from .views import AdminDeleteClient, AdminDeleteSecret


urlpatterns = {
    # REST Patterns for all users
    url(r'^GetCredential$', GetCredentialView.as_view(), name="get_cred"),
    url(r'^NewClientId$', NewClientId.as_view(), name="new_client"),

    # Full User Front End Url Patterns
    # ToDo: Build a user frontend so that the AdminSite is not the only place to
    # ToDo: cont'd .. make changes to model entries
    # CreateClient is a Future release feature
    url(r'^CreateClient$', CreateClientView.as_view(), name="create_client"),
    # UpdateClient is a Future release feature
    url(r'^UpdateClient$', UpdateClientView.as_view(), name="update_client"),

    # ADMIN patterns for is_staff users
    url(r'^admin/GetAllClients$', AdminGetClientsView.as_view(), name="adm_all_clients"),
    url(r'^admin/GetAllSecrets$', AdminGetSecretsView.as_view(), name="adm_all_secrets"),
    url(r'^admin/GetClient$', AdminGetClientView.as_view(), name="adm_client"),
    url(r'^admin/GetSecret$', AdminGetSecretView.as_view(), name="adm_secret"),
    url(r'^admin/GetSecretClients$', AdminGetSecretClientsView.as_view(), name="adm_secret_client"),
    url(r'^admin/DeleteClient$', AdminDeleteClient.as_view(), name="adm_del_client"),
    url(r'^admin/DeleteSecret$', AdminDeleteSecret.as_view(), name="adm_del_secret"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
