from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from management_email.models import Mailingattempt


class Command(BaseCommand):
    help = 'Отправляет рассылку'

    def add_arguments(self, parser):
        parser.add_argument('subject', type=str, help='Тема рассылки')
        parser.add_argument('message', type=str, help='Сообщение для рассылки')
        parser.add_argument('recipients', type=str, nargs='+', help='Список адресов получателей')

    def handle(self, *args, **kwargs):
        subject = kwargs['subject']
        message = kwargs['message']
        from_email = kwargs['from_email']
        recipients = kwargs['recipients']

        # Отправка почты
        send_mail(subject, message, from_email, recipients)

        # Запись информации о рассылке в базу данных
        Mailingattempt.objects.create(subject=subject, message=message, status='успешно')

        self.stdout.write(self.style.SUCCESS('Рассылка успешно отправлена.'))
