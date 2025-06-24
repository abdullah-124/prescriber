from django.core.mail import EmailMessage
import logging

def send_approval_mail(name, text,email_address):
    try:
        html_message = f"""
        <h2>Hello {name},</h2>
        <p>{text}</p>
        """

        email = EmailMessage(
            subject="Doctor Application Approval Mail",
            body=html_message,
            from_email='website.prescriber@gmail.com',
            to=[email_address]
        )
        email.content_subtype = "html"
        email.send()
        return True
    except Exception as e:
        logging.error(f"Email sending failed: {e}")
        return False