from django.urls import path
from management_email.apps import ManagementEmailConfig
from management_email.views import home

app_name = ManagementEmailConfig.name

urlpatterns = [
    path('', home, name='home'),
]
