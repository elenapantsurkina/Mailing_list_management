from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Customers, Message, Mailing, Mailingattempt
from .forms import CustomersForm, MailingForm, MessageForm
from django.shortcuts import render
from django.core.mail import send_mail
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from users.services import get_mailing_statistics
from django.views.decorators.cache import cache_page


@cache_page(60 * 15)
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


class MailingattemptListView(LoginRequiredMixin, ListView):
    model = Mailingattempt
    template_name = "management_email/mailingattempt_list.html"
    context_object_name = 'object_list'  # Имя списка для передачи в шаблон

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Manager").exists():
            pass
        self.send_mail_for_clients()
        return Mailingattempt.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_mailings = Mailing.objects.count()  # Общее количество рассылок
        active_mailings = Mailing.objects.filter(status='запущена').count()  # Количество активных рассылок
        unique_recipients = Customers.objects.distinct().count()  # Количество уникальных получателей

        context['total_mailings'] = total_mailings,
        context['active_mailings'] = active_mailings,
        context['unique_recipients'] = unique_recipients,

        context['statistics'] = get_mailing_statistics(self.request.user)
        return context

    def send_mail_for_clients(self):
        # Получаем объект рассылки по идентификатору
        user = self.request.user
        mailings = Mailing.objects.filter(owner=user.id)

        # Получаем список клиентов из ManyToMany поля
        customers = [mailing.customers.all() for mailing in mailings]
        total_attempts = 0
        successful_attempts = 0
        failed_attempts = 0

        for mailing, customer_list in zip(mailings, customers):

            for customer in customer_list:
                total_attempts += 1
                try:
                    response = send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.body,
                        from_email='elenapantsurkina@yandex.ru',
                        recipient_list=[customer.email],
                        fail_silently=False,
                    )
                    successful_attempts += 1

                    # Создаем запись о попытке рассылки
                    Mailingattempt.objects.create(
                        mailing=mailing,
                        status="успешно",
                        mail_server_response=str(response),
                        date_attempt=timezone.now(),
                    )
                except Exception as e:
                    failed_attempts += 1
                    # Создаем запись о неудачной попытке рассылки
                    Mailingattempt.objects.create(
                        mailing=mailing,
                        status="неуспешно",
                        mail_server_response=str(e),
                        date_attempt=timezone.now(),
                    )

        stats = {
            'total_attempts': total_attempts,
            'successful_attempts': successful_attempts,
            'failed_attempts': failed_attempts,
        }
        return stats
