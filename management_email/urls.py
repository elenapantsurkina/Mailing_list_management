from django.urls import path
from management_email.views import home
from management_email.apps import ManagementEmailConfig
from management_email.views import (
    CustomersCreateView,
    CustomersListView,
    CustomersDetailView,
    CustomersUpdateView,
    CustomersDeleteView,
)
from management_email.views import (
    MessageCreateView,
    MessageListView,
    MessageDetailView,
    MessageUpdateView,
    MessageDeleteView,
)
from management_email.views import (
    MailingCreateView,
    MailingListView,
    MailingDetailView,
    MailingUpdateView,
    MailingDeleteView,
)


app_name = ManagementEmailConfig.name

urlpatterns = [
    path("", home, name="home"),
    path(
        "management_email/customers_list/",
        CustomersListView.as_view(),
        name="customers_list",
    ),
    path(
        "management_email/customers_detail/<int:pk>/",
        CustomersDetailView.as_view(),
        name="customers_detail",
    ),
    path(
        "management_email/customers_create/",
        CustomersCreateView.as_view(),
        name="customers_create",
    ),
    path(
        "management_email/customers_update/<int:pk>",
        CustomersUpdateView.as_view(),
        name="customers_update",
    ),
    path(
        "management_email/customers_delete/<int:pk>/",
        CustomersDeleteView.as_view(),
        name="customers_delete",
    ),
    path(
        "management_email/message_list/", MessageListView.as_view(), name="message_list"
    ),
    path(
        "management_email/message/<int:pk>/",
        MessageDetailView.as_view(),
        name="message_detail",
    ),
    path(
        "management_email/message_create/",
        MessageCreateView.as_view(),
        name="message_create",
    ),
    path(
        "management_email/message_update/<int:pk>/",
        MessageUpdateView.as_view(),
        name="message_update",
    ),
    path(
        "management_email/message_delete/<int:pk>/",
        MessageDeleteView.as_view(),
        name="message_delete",
    ),
    path(
        "management_email/mailing_list/", MailingListView.as_view(), name="mailing_list"
    ),
    path(
        "management_email/mailing_detail/<int:pk>/",
        MailingDetailView.as_view(),
        name="mailing_detail",
    ),
    path(
        "management_email/mailing_create/",
        MailingCreateView.as_view(),
        name="mailing_create",
    ),
    path(
        "management_email/mailing_update/<int:pk>/",
        MailingUpdateView.as_view(),
        name="mailing_update",
    ),
    path(
        "management_email/mailing_delete/<int:pk>/",
        MailingDeleteView.as_view(),
        name="mailing_delete",
    ),
]
