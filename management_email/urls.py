from django.urls import path
from management_email.views import home
from management_email.apps import ManagementEmailConfig
from management_email.views import (CustomersCreateView, CustomersListView,
                                    CustomersDetailView, CustomersUpdateView, CustomersDeleteView)
from management_email.views import (MessageCreateView, MessageListView,
                                    MessageDetailView, MessageUpdateView, MessageDeleteView)
from management_email.views import (MailingCreateView, MailingListView,
                                    MailingDetailView, MailingUpdateView, MailingDeleteView)


app_name = ManagementEmailConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('customers/', CustomersListView.as_view(), name='customers_list'),
    path('customers/<int:pk>/', CustomersDetailView.as_view(), name='customers_detail'),
    path('customers/new/', CustomersCreateView.as_view(), name='customers_create'),
    path('customers/<int:pk>/update/', CustomersUpdateView.as_view(), name='customers_update'),
    path('customers/<int:pk>/delete/', CustomersDeleteView.as_view(), name='customers_delete'),
    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/new/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
    path('mailing/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/new/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
]
