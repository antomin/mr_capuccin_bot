from django.conf import settings

from tgbot_app.loader import bot
from tgbot_app.utils.common import parse_daily_result, parse_weekly_result
from tgbot_app.utils.db_api import get_daily_task_info, get_weekly_task_info


async def daily_report_scheduler() -> None:
    result = await get_daily_task_info()

    text = await parse_daily_result(result)

    for admin in settings.ADMINS:
        await bot.send_message(chat_id=admin, text=text)


async def weekly_report_scheduler() -> None:
    result = await get_weekly_task_info()

    text = await parse_weekly_result(result)

    for admin in settings.ADMINS:
        await bot.send_message(chat_id=admin, text=text)
