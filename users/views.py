from django.views.generic import CreateView
from users.models import User
from users.forms import UserRegisterForm
from django.urls import reverse_lazy


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")
