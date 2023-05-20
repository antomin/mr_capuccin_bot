from aiogram import Dispatcher
from aiogram.utils import executor
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand

from tgbot_app.filters import NoOpenSessions
from tgbot_app.handlers import dp
from tgbot_app.loader import scheduler
from tgbot_app.middlewares import IsWorkerMiddleware
from tgbot_app.shedulers import daily_report_scheduler, weekly_report_scheduler
from tgbot_app.utils.set_commands import set_default_commands


async def register_middlewares(_dp: Dispatcher):
    _dp.setup_middleware(IsWorkerMiddleware())


async def register_filters(_dp: Dispatcher):
    _dp.filters_factory.bind(NoOpenSessions)


async def on_startup(_dp: Dispatcher):
    await set_default_commands(_dp)
    await register_middlewares(_dp)
    await register_filters(_dp)

    scheduler.add_job(daily_report_scheduler, trigger=CronTrigger(hour='23'))
    scheduler.add_job(weekly_report_scheduler, trigger=CronTrigger(hour='23', day_of_week='sun'))
    scheduler.start()


class Command(BaseCommand):
    def handle(self, *args, **options):
        executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
