# Generated by Django 4.2.2 on 2024-12-06 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("management_email", "0004_message_owner"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="mailing",
            options={
                "permissions": [("can_cancel_mailing", "Can cancel mailing")],
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
            },
        ),
    ]
