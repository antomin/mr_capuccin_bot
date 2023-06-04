from datetime import datetime, timedelta

from asgiref.sync import sync_to_async
from django.db.models import QuerySet

from report_app.models import DailyReport, Task
from tgbot_app.models import Store, Worker, WorkSession, AdminReport


@sync_to_async
def get_workers_id() -> list:
    workers = Worker.objects.all()
    return [worker.tgid for worker in workers]


@sync_to_async
def get_worker(tgid: str) -> Worker:
    return Worker.objects.filter(tgid=tgid).first()


@sync_to_async
def get_store(store_id: str = None, user_id: int = None) -> Store:
    if store_id:
        return Store.objects.get(id=store_id)
    if user_id:
        work_session = WorkSession.objects.filter(worker_id=user_id, is_open=True).first()
        return work_session.store
    return Store.objects.all()


@sync_to_async
def get_current_tasks(user_id: int) -> QuerySet:
    work_session = WorkSession.objects.filter(worker_id=user_id, is_open=True).first()
    tasks = work_session.tasks.filter(out_of_time=False)
    return tasks


@sync_to_async
def get_task(task_id: int) -> Task:
    return Task.objects.get(id=task_id)


@sync_to_async()
def need_confirm(task: Task) -> bool:
    return task.task_type.need_confirmation


@sync_to_async
def get_work_session(user_id: int = None, work_session_id: int = None) -> WorkSession:
    if user_id:
        return WorkSession.objects.filter(is_open=True, worker_id=user_id).first()
    if work_session_id:
        return WorkSession.objects.get(id=work_session_id)


@sync_to_async
def create_work_session(store_id: int, user_id: int) -> int:
    store = Store.objects.get(id=store_id)
    work_session = WorkSession(worker_id=user_id, store_id=store_id)
    work_session.save()

    for task_type in store.task_types.all():
        task = Task(task_type=task_type, work_session=work_session)
        if task_type.time_exec not in ('morning', 'all_day'):
            task.out_of_time = True
        task.save()

    return work_session.id


@sync_to_async
def check_img_unique(md5: str) -> bool:
    md5_list = [task.img_hash for task in Task.objects.all() if task.img_hash]
    return not (md5 in md5_list)


@sync_to_async
def confirm_task(task_id, path_img=None, md5_img=None) -> None:
    task = Task.objects.get(id=task_id)
    if path_img:
        task.img_confirmation = path_img
        task.img_hash = md5_img
    task.completed_at = datetime.now()
    task.is_completed = True
    task.save()


@sync_to_async
def user_is_busy(user_id: int) -> bool:
    return True if WorkSession.objects.filter(is_open=True, worker_id=user_id) else False


@sync_to_async
def change_work_session_worker(old_user_id: int, new_user_id: int) -> bool:
    try:
        new_worker = Worker.objects.get(tgid=new_user_id)
        old_worker = Worker.objects.get(tgid=old_user_id)

        work_session = WorkSession.objects.filter(is_open=True, worker=old_worker).last()
        work_session.worker = new_worker
        work_session.comment += f'{new_worker.first_name} {new_worker.last_name} сменил ' \
                                f'{old_worker.first_name} {old_worker.last_name} в {datetime.now().strftime("%H:%M")}\n'
        work_session.save()

        return True
    except Exception:
        return False


@sync_to_async
def change_tasks(work_session: WorkSession, time_exec: str) -> None:
    time_exec_rules = {'morning': 'midday', 'midday': 'evening', 'evening': None}

    current_tasks = work_session.tasks.filter(out_of_time=False, task_type__time_exec=time_exec)

    for task in current_tasks:
        task.out_of_time = True
        task.save()

    next_time_exec = time_exec_rules[time_exec]

    if next_time_exec:
        next_tasks = work_session.tasks.filter(out_of_time=True, task_type__time_exec=next_time_exec)

        for task in next_tasks:
            task.out_of_time = False
            task.save()
    else:
        all_open_tasks = work_session.tasks.filter(out_of_time=False)

        for task in all_open_tasks:
            task.out_of_time = True
            task.save()

        work_session.close_time = datetime.now()
        work_session.is_open = False
        work_session.save()


@sync_to_async
def get_daily_task_info() -> dict:
    result = {}

    for store in Store.objects.all():
        result[store.title] = {}
        work_session = WorkSession.objects.filter(store=store, open_time__day=datetime.today().day,
                                                  open_time__month=datetime.today().month).first()
        if not work_session:
            continue

        unfulfilled_tasks = Task.objects.filter(work_session=work_session, is_completed=False)
        unfulfilled_tasks_titles = [task.task_type.title for task in unfulfilled_tasks]
        tasks_cnt = Task.objects.filter(work_session=work_session).count()

        result[store.title]['worker'] = f'{work_session.worker.first_name} {work_session.worker.last_name}'
        result[store.title]['tasks_cnt'] = tasks_cnt
        result[store.title]['unfulfilled_cnt'] = unfulfilled_tasks.count()
        result[store.title]['unfulfilled_tasks'] = unfulfilled_tasks_titles

        daily_report = DailyReport(store=store, tasks_cnt=tasks_cnt)
        if unfulfilled_tasks.count():
            daily_report.is_perfect = False
            daily_report.unfulfilled_tasks = '\n'.join(unfulfilled_tasks_titles)
        daily_report.save()

    return result


@sync_to_async
def get_weekly_task_info() -> dict:
    result = {}

    for store in Store.objects.all():
        result[store.title] = {}

        _today = datetime.today()
        reports = DailyReport.objects.filter(created_at__lte=_today, created_at__gte=_today - timedelta(days=7),
                                             store=store)
        unfulfilled_tasks_list = []
        for report in reports.filter(is_perfect=False):
            unfulfilled_tasks_list += report.unfulfilled_tasks.split('\n')

        result[store.title]['unfulfilled_tasks'] = []
        for task in set(unfulfilled_tasks_list):
            result[store.title]['unfulfilled_tasks'].append((task, unfulfilled_tasks_list.count(task)))

        result[store.title]['perfect_days'] = reports.filter(is_perfect=True).count()

    return result


@sync_to_async
def get_admins():
    admins = AdminReport.objects.all()
    return [admin.tgid for admin in admins]
