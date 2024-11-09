import os
from sendgrid import From, SendGridAPIClient
from sendgrid.helpers.mail import Mail

from utils.environment import get_env_var

SENDGRID_SENDER = get_env_var("SENDGRID_SENDER")
SENDGRID_API_KEY = get_env_var("SENDGRID_API_KEY")


def send_email(to, subject, template_id, dynamic_template_data):
    message = Mail(
        from_email=From(os.environ.get("SENDGRID_SENDER"), "Basel"),
        to_emails=to,
        subject=subject,
    )
    message.template_id = template_id
    message.dynamic_template_data = dynamic_template_data

    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
