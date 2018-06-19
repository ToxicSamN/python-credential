# api/urls.py

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import GetCredentialView, AdminGetClientsView, AdminGetClientView
from.frontend_views import CreateClientView, UpdateClientView
from .views import AdminGetSecretsView, AdminGetSecretView, AdminGetSecretClientsView
from .views import AdminDeleteClient, AdminDeleteSecret


urlpatterns = {
    url(r'^GetCredential$', GetCredentialView.as_view(), name="get_cred"),
    url(r'^CreateClient$', CreateClientView.as_view(), name="create_client"),
    url(r'^UpdateClient$', UpdateClientView.as_view(), name="update_client"),
    url(r'^admin/GetAllClients$', AdminGetClientsView.as_view(), name="adm_all_clients"),
    url(r'^admin/GetAllSecrets$', AdminGetSecretsView.as_view(), name="adm_all_secrets"),
    url(r'^admin/GetClient$', AdminGetClientView.as_view(), name="adm_client"),
    url(r'^admin/GetSecret$', AdminGetSecretView.as_view(), name="adm_secret"),
    url(r'^admin/GetSecretClients$', AdminGetSecretClientsView.as_view(), name="adm_secret_client"),
    url(r'^admin/DeleteClient$', AdminDeleteClient.as_view(), name="adm_del_client"),
    url(r'^admin/DeleteSecret$', AdminDeleteSecret.as_view(), name="adm_del_secret"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
