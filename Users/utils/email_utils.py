from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from Users.custom_exceptions import SendGridException


class EmailUtils:
    def __init__(self):
        self.from_email_address = os.getenv("FROM_EMAIL_ADDRESS")
        self.send_grid_client = SendGridAPIClient(api_key='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')


    def send_email(self, subject, html_content, to_emails, from_email_address=None):
        try:
            if not from_email_address:
                from_email_address = self.from_email_address
            message = Mail(
            from_email=from_email_address,
            to_emails=to_emails,
            subject=subject,
            html_content=html_content)
            response = self.send_grid_client.send(message)
        except Exception as err:
            raise SendGridException(f"Oops Something went wrong : {err}")