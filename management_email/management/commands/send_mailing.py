from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from management_email.models import Mailingattempt


class Command(BaseCommand):
    help = 'Отправляет рассылку'

    def add_arguments(self, parser):
        parser.add_argument('subject', type=str, help='Тема рассылки')
        parser.add_argument('message', type=str, help='Сообщение для рассылки')

    def handle(self, *args, **kwargs):
        subject = kwargs['subject']
        message = kwargs['message']
        recipients = ['recipient@example.com']  # Здесь можно также получить список получателей

        # Отправка почты
        send_mail(subject, message, 'from@example.com', recipients)

        # Запись информации о рассылке в базу данных
        Mailingattempt.objects.create(subject=subject, message=message, status='успешно')

        self.stdout.write(self.style.SUCCESS('Рассылка успешно отправлена.'))
