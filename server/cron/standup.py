import logging
import aiocron
from database.user import User
from mailer import send_email


logger = logging.getLogger(__name__)


async def send_daily_standup_reminder():
    logger.debug("SENDING DAILY STANDUP REMINDER")
    try:
        users = await User.find(User.status == True).to_list()
        emails = [user.email for user in users]
        logger.debug(f"TO EMAILS: {emails}")
        send_email(
            emails=emails,
            template_id="d-874f7b08932343f087ca6fa936823eed",
            dynamic_template_data=None,
        )
    except Exception as e:
        logger.error(e)


@aiocron.crontab("0 0 * * 1-5")
async def trigger_send_daily_standup_reminder():
    await send_daily_standup_reminder()
