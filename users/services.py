from management_email.models import Mailingattempt, Mailing


def get_mailing_statistics(user):
    # подсчет количества успешных и неуспешных попыток
    successful_attempts = Mailingattempt.objects.filter(mailing__owner=user, status='успешно').count()
    unsuccessful_attempts = Mailingattempt.objects.filter(mailing__owner=user, status='неуспешно').count()
    sent_messages = Mailing.objects.filter(owner=user).count()
    return {
        'successful_attempts': successful_attempts,
        'unsuccessful_attempts': unsuccessful_attempts,
        'sent_messages': sent_messages,
    }
