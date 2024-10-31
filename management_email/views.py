from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import Customers, Message, Mailing
from django.shortcuts import render


def home(request):
    return render(request, 'management_email/home.html')


class CustomersCreateView(CreateView):
    model = Customers
    fields = ['name', 'email', 'comment']
    template_name = 'customers_form.html'
    success_url = reverse_lazy('customers_list')


class CustomersListView(ListView):
    model = Customers
    template_name = 'customers_list.html'


class CustomersDetailView(DetailView):
    model = Customers
    template_name = 'customers_detail.html'


class CustomersUpdateView(UpdateView):
    model = Customers
    fields = ['name', 'email', 'comment']
    template_name = 'customers_form.html'
    success_url = reverse_lazy('customers_list')


class CustomersDeleteView(DeleteView):
    model = Customers
    template_name = 'customers_confirm_delete.html'
    success_url = reverse_lazy('customers_list')


class MessageCreateView(CreateView):
    model = Message
    fields = ['heading', 'content']
    template_name = 'message_form.html'
    success_url = reverse_lazy('message_list')


class MessageListView(ListView):
    model = Message
    template_name = 'message_list.html'


class MessageDetailView(DetailView):
    model = Message
    template_name = 'message_detail.html'


class MessageUpdateView(UpdateView):
    model = Message
    fields = ['heading', 'content']
    template_name = 'message_form.html'
    success_url = reverse_lazy('message_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'message_confirm_delete.html'
    success_url = reverse_lazy('message_list')


class MailingCreateView(CreateView):
    model = Mailing
    fields = ['heading', 'status']
    template_name = 'mailing_form.html'
    success_url = reverse_lazy('mailing_list')


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing_list.html'


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing_detail.html'


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['heading', 'status']
    template_name = 'mailing_form.html'
    success_url = reverse_lazy('mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_list')
