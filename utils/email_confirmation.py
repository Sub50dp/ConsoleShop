from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from Console.settings import EMAIL_HOST_USER


class EmailConfirmationSender:
    @staticmethod
    def send_confirmation_email(user_email, confirmation_link):
        subject = 'Confirm your email'
        html_message = render_to_string('users/email_confirmation.html', {'confirmation_link': confirmation_link})
        plain_message = strip_tags(html_message)
        from_email = EMAIL_HOST_USER
        to_email = user_email

        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
