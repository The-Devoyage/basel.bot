from typing import List
from python_http_client.client import logging
from sendgrid import From, Personalization, SendGridAPIClient, To
from sendgrid.helpers.mail import Mail

from utils.environment import get_env_var

logger = logging.getLogger(__name__)

# Constants
SENDGRID_SENDER = get_env_var("SENDGRID_SENDER")
SENDGRID_API_KEY = get_env_var("SENDGRID_API_KEY")


def send_email(emails: List[str], template_id: str, dynamic_template_data):
    logger.debug("SENDING EMAIL")
    message = Mail(
        from_email=From(SENDGRID_SENDER, "Basel"),
    )
    message.template_id = template_id

    # Add personalizations for each recipient
    for email in emails:
        personalization = Personalization()
        to = To(email)
        personalization.add_to(to)
        message.add_personalization(personalization)
        if dynamic_template_data is not None:
            personalization.dynamic_template_data = dynamic_template_data

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
