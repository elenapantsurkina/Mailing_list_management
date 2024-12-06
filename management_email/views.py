from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Customers, Message, Mailing, Mailingattempt
from .forms import CustomersForm, MailingForm, MessageForm
from django.shortcuts import render
from django.core.mail import send_mail
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse


def home(request):
    total_mailings = Mailing.objects.count()  # Общее количество рассылок
    active_mailings = Mailing.objects.filter(status='запущена').count()  # Количество активных рассылок
    unique_recipients = Customers.objects.distinct().count()  # Количество уникальных получателей

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_recipients': unique_recipients,
    }

    return render(request, "management_email/home.html", context)


class CustomersCreateView(CreateView, LoginRequiredMixin):
    model = Customers
    form_class = CustomersForm
    template_name = "management_email/customers_form.html"
    success_url = reverse_lazy("management_email:customers_list")

    def form_valid(self, form):
        customer = form.save()
        user = self.request.user
        customer.owner = user
        customer.save()
        return super().form_valid(form)


class CustomersListView(ListView, LoginRequiredMixin):
    model = Customers
    template_name = "management_email/customers_list.html"

    def get_queryset(self):
        # Проверяем, является ли пользователь менеджером или автором клиента
        if self.request.user.is_staff:  # Менеджеры имеют доступ ко всем клиентам
            return Customers.objects.all()
        return Customers.objects.filter(owner=self.request.user)  # Показываем только клиентов пользователя


class CustomersDetailView(DetailView, LoginRequiredMixin):
    model = Customers
    template_name = "management_email/customers_detail.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not (self.request.user.is_staff or obj.owner == self.request.user):
            raise PermissionDenied  # Отказать доступ, если не менеджер или не владелец
        return obj


class CustomersUpdateView(UpdateView):
    model = Customers
    form_class = CustomersForm
    template_name = "management_email/customers_form.html"
    success_url = reverse_lazy("management_email:customers_list")

    def get_queryset(self):
        if self.request.user.is_staff:
            return Customers.objects.all()
        return Customers.objects.filter(owner=self.request.user)


class CustomersDeleteView(DeleteView):
    model = Customers
    template_name = "management_email/customers_confirm_delete.html"
    success_url = reverse_lazy("management_email:customers_list")

    def get_queryset(self):
        if self.request.user.is_staff:
            return Customers.objects.all()
        return Customers.objects.filter(owner=self.request.user)


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = "management_email/message_form.html"
    success_url = reverse_lazy("management_email:message_list")

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageListView(ListView):
    model = Message
    template_name = "management_email/message_list.html"

    def get_queryset(self):
        if self.request.user.is_staff:
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(DetailView):
    model = Message
    template_name = "management_email/message_detail.html"

    def get_queryset(self):
        if self.request.user.is_staff:
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "management_email/message_form.html"
    success_url = reverse_lazy("management_email:message_list")

    def test_func(self):
        message = self.get_object()  # Получаем текущий объект
        return self.request.user == message.owner


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "management_email/message_confirm_delete.html"
    success_url = reverse_lazy("management_email:message_list")

    def test_func(self):
        message = self.get_object()  # Получаем текущий объект
        return self.request.user == message.owner


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "management_email/mailing_form.html"
    success_url = reverse_lazy("management_email:mailing_list")

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingListView(ListView):
    model = Mailing
    template_name = "management_email/mailing_list.html"

    def get_queryset(self):
        if self.request.user.is_staff:
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(DetailView):
    model = Mailing
    template_name = "management_email/mailing_detail.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not (self.request.user.is_staff or obj.owner == self.request.user):
            raise PermissionDenied  # Отказать доступ
        return obj


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "management_email/mailing_form.html"
    success_url = reverse_lazy("management_email:mailing_list")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "management_email/mailing_confirm_delete.html"
    success_url = reverse_lazy("management_email:mailing_list")


class SendMailingView(View):
    # реализуем отправку через интерфейс пользователя
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.send_mailing()  # Вызов метода для отправки

        mailing.status = "запущена"  # Обновляем статус рассылки
        mailing.save()  # Сохраняем изменения в модели

        return redirect(reverse("management_email:mailing_list"))  # Перенаправление после отправки


class CancelMailingView(LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        if not request.user.has_perm('management_email.can_cancel_mailing'):
            return HttpResponseForbidden("У вас нет прав для отключения рассылки.")
            # Логика отключения рассылки
        mailing.status = "завершена"
        mailing.save()
        return redirect("management_email:mailing_list")


class BlokMailingView(LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        if not request.user.has_perm('management_email.can_blok_user'):
            return HttpResponseForbidden("У вас нет прав для отключения рассылки.")
            # Логика отключения рассылки
        mailing.status = "завершена"
        mailing.save()
        return redirect("management_email:mailing_list")


class MailingattemptListView(ListView):
    model = Mailingattempt
    template_name = "management_email/mailingattempt_list.html"

    def send_mail_for_clients(mailing_id):
        # Получаем объект рассылки по идентификатору
        mailing = Mailing.objects.get(id=mailing_id)
        # Получаем список клиентов из ManyToMany поля
        customers = mailing.customers.all()
        total_attempts = mailing.mailings.count()

        for customer in customers:
            try:
                response = send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=mailing.message.from_email,
                    recipient_list=[customer.email],
                    fail_silently=False,
                    )

            # Создаем запись о попытке рассылки
                Mailingattempt.objects.create(
                    mailing=mailing,
                    status="успешно",
                    mail_server_response=str(response),
                    date_attempt=timezone.now(),
                    total_attempts=total_attempts + 1,
                )
            except Exception as e:
                # Создаем запись о неудачной попытке рассылки
                Mailingattempt.objects.create(
                    mailing=mailing,
                    status="неуспешно",
                    mail_server_response=str(e),
                    date_attempt=timezone.now(),
                    total_attempts=total_attempts + 1
                )
