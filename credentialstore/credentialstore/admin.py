
from django.contrib.admin.sites import AdminSite


class CustomAdminSite(AdminSite):
    site_header = "Sammy'''s Playground"
    site_title = "My SuperCool Title"
