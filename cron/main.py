from datetime import datetime
import aiocron
import asyncio
import httpx
from utils.environment import get_env_var

MAILER_API_KEY = get_env_var("MAILER_API_KEY")
SERVER_URL = get_env_var("SERVER_URL")

HOLIDAYS = [
    "01-01",
    "12-25",
]


# Function to check if today is a holiday
def is_holiday():
    today = datetime.today().strftime("%m-%d")
    return today in HOLIDAYS


# Function to send the daily standup reminder
async def send_daily_standup_reminder():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                SERVER_URL + "/mailer/daily-standup-reminder",
                headers={"api-key": f"{MAILER_API_KEY}"},
            )
            if response.status_code == 200:
                print("Daily standup reminder sent successfully.")
            else:
                print(f"Failed to send reminder. Status code: {response.status_code}")
        except httpx.RequestError as e:
            print(f"An error occurred while sending the reminder: {e}")


@aiocron.crontab("0 0 * * 1-5")
async def trigger_send_daily_standup_reminder():
    if is_holiday():
        print("Today is a holiday. Skipping the reminder.")
        return
    await send_daily_standup_reminder()


asyncio.get_event_loop().run_forever()
