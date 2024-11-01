from django.db import models


class Customers(models.Model):
    email = models.EmailField(unique=True, verbose_name='email', help_text='Введите электронную почту')
    name = models.CharField(max_length=100, verbose_name='Ф.И.О.', help_text='Введите Фамилию Имя Очество')
    comment = models.TextField(blank=True, null=True, help_text='Добавьте комментарии')

    def __str__(self):
        return f'{self.name} {self.email}'

    class Meta:
        verbose_name = 'Получатель рассылки'
        verbose_name_plural = 'Получатели рассылок'
        ordering = ['email']
        db_table = 'Mailing'


class Message(models.Model):
    heading = models.CharField(max_length=150, verbose_name='Тема письма', help_text='Введите тему письма')
    content = models.TextField(blank=True, null=True, help_text='Введите текст письма')

    def __str__(self):
        return self.heading

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    date_first = models.DateTimeField(auto_now=True, verbose_name='Дата и время первой отправки')
    date_end = models.DateTimeField(auto_now=True, verbose_name='Дата и время окончания отправки')
    STATUS_CHOICES = [
        ('создана', 'Создана'),
        ('запущена', 'Запущена'),
        ('завершена', 'Завершена'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='создана')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='messages')
    customers = models.ManyToManyField(Customers)

    def __str__(self):
        return f'{self.message} - {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Mailingattempt(models.Model):
    date_attempt = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = [
        ('успешно', 'Успешно'),
        ('неуспешно', 'Неуспешно'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    mail_server_response = models.TextField(blank=True, null=True, help_text='Ответ почтового сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='mailings')

    def __str__(self):
        return f'Попытка: {self.status} - {self.date_attempt}'

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылок'
