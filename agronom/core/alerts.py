from django.core.mail import send_mail
from django.conf import settings

from .logging import getLogger


# TODO: переделать на https://docs.djangoproject.com/en/2.1/topics/logging/


def send_alert(module_name, message, send_email=True, send_sms=False):
    logger = getLogger(module_name)
    logger.error(message)

    msg = 'Module_name: {}\r\nMessage: {}'.format(module_name, message)
    if send_email:
        send_alert_through_email(module_name, message)
    if send_sms:
        send_alert_through_sms(msg)


def send_alert_through_email(subject, msg):
    mail_sent_counter = send_mail(
        subject,
        msg,
        settings.DEFAULT_FROM_EMAIL,
        settings.ALERTS_EMAILS,
        fail_silently=False,
    )

    return mail_sent_counter == len(settings.ALERTS_EMAILS)


def send_alert_through_sms(msg):
    raise NotImplementedError("Sending alerts through SMS is not implemented yet")
