from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('users/', include('django.contrib.auth.urls')),
    path(
        "",
        include(
            ("management_email.urls", "management_email"), namespace="management_email"
        ),
    ),
    path("users/", include("users.urls", namespace="users")),
]
