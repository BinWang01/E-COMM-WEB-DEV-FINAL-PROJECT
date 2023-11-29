from django.contrib.admin.apps import AdminConfig

class DataAdminConfig(AdminConfig):
    default_site = 'django_project.admin.DataAdminSite'