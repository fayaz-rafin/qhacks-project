# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
import dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

dotenv.load_dotenv()


def send_email(to_email: str, subject: str, message: str):
    message = Mail(
        from_email=os.environ.get('SENDGRID_FROM_EMAIL'),
        to_emails=to_email,
        subject=subject,
        html_content=message)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return response.status_code
    except Exception as e:
        print(e.message)