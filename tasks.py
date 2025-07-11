import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from alx_travel_app.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD


def send_email(recipient_list, subject, message_plain, message_html):
    """
    Function to send an email using Django's send_mail utility.
    """
    for recipient in recipient_list:
        try:
            email_msg = MIMEMultipart("alternative")
            email_msg["Subject"] = subject
            email_msg["From"] = 'noreply@gmail.com'
            email_msg["To"] = recipient

            text_part = MIMEText(message_plain, "plain")
            html_part = MIMEText(message_html, "html")
            email_msg.attach(text_part)
            email_msg.attach(html_part)

            server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            server.starttls()
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.sendmail(EMAIL_HOST_USER, recipient_list, email_msg.as_string())
            server.quit()

        except Exception as e:
            print(f"Failed to send email: {e}")