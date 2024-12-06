from audioop import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,View
from users.models import User
from users.forms import UserRegisterForm
from django.urls import reverse_lazy
import secrets
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from django.shortcuts import get_object_or_404, redirect, render
from management_email.models import Mailingattempt
from .services import get_mailing_statistics
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("management_email:home")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Приветствую. Перейдите по ссылке для подтверждения почты {url} ",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )

        return super().form_valid(form)


class UserBlokView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if not request.user.has_perm('users.can_blok_user'):
            return HttpResponseForbidden("У вас нет прав для отключения рассылки.")
            # Логика ,блокировки пользователя
        user.is_active = not user.is_active
        user.save()
        return redirect("users:users")


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


@login_required
def mailing_attempts_view(request):
    mailingattempts = Mailingattempt.objects.filter(mailing__owner=request.user)
    statistics = get_mailing_statistics(request.user)  # Вызовите функцию

    return render(request, 'mailingattempt_list.html',
                  {'mailingattempts': mailingattempts, 'statistics': statistics})
