from django.core.mail import send_mail

from celery import shared_task

from alx_travel_app.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD


@shared_task
def send_email(recipient_list, subject, message_plain):
    try:
        send_mail(
            subject=subject,
            message=message_plain,
            from_email=EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        print(f"Email sent to {recipient_list}")
    except Exception as e:
        print(f"Failed to send email: {e}")
