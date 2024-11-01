from django.contrib import admin

from .models import Customers, Message, Mailing, Mailingattempt

admin.site.register(Customers)
admin.site.register(Message)
# admin.site.register(Mailing)
admin.site.register(Mailingattempt)


@admin.register(Mailing)
class Mailingadmin(admin.ModelAdmin):
    list_display = ("date_first", "date_end", "status", "message")
    list_filter = ("status",)
    search_fields = ("status",)
