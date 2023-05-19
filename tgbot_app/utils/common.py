from datetime import datetime

from tgbot_app.models import Store


async def get_dt_for_scheduler(store: Store) -> dict:
    date_now = datetime.now()
    morning_time = await store.get_time_exec('morning')
    midday_time = await store.get_time_exec('midday')
    evening_time = await store.get_time_exec('evening')

    return {
        'morning': datetime(date_now.year, date_now.month, date_now.day, morning_time.hour, morning_time.minute),
        'midday': datetime(date_now.year, date_now.month, date_now.day, midday_time.hour, midday_time.minute),
        'evening': datetime(date_now.year, date_now.month, date_now.day, evening_time.hour, evening_time.minute)
    }


async def parse_daily_result(result: dict) -> str:
    text = f'<b>Отчёт за {datetime.today().strftime("%d.%m.%Y")}:</b>\n\n'

    for store, info in result.items():
        text += f'<b>{store}:</b>\n'

        if not info:
            text += 'Нет информации.\n\n'
            continue

        text += f'Сотрудник: <i>{info["worker"]}</i>\n'

        if info['unfulfilled_cnt'] == 0:
            text += 'Все задачи выполнены.\n\n'
            continue

        text += f'Выполнено: <i>{info["tasks_cnt"] - info["unfulfilled_cnt"]} из {info["tasks_cnt"]}</i>\n' \
                f'Невыполненные задачи:\n'

        for task in info['unfulfilled_tasks']:
            text += f'<i>- {task}</i>\n'

        text += '\n'

    return text


async def parse_weekly_result(result: dict) -> str:
    text = '<b>Недельный отчёт:</b>\n\n'

    for store, info in result.items():
        text += f'<b>{store}:</b>\n'

        if info["perfect_days"] == 0 and not info['unfulfilled_tasks']:
            text += 'Нет информации.\n\n'
            continue

        text += f'Дней с полностью выполненными задачами: <i>{info["perfect_days"]}</i>.\n\n'

        if info['unfulfilled_tasks']:
            text += 'Не выполнено:\n'
            for task in info['unfulfilled_tasks']:
                text += f'<i>- {task[0]} ({task[1]})</i>\n'

        text += '\n'

    return text
