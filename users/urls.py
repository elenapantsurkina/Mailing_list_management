from django.urls import path
from users.apps import UsersConfig
from django.contrib.auth.views import LoginView

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"))

]