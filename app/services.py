from typing import Iterable

from app import app
from app.models import Task
from app.types import TaskOrderBy


def get_tasks(page: int = 1, order_by: TaskOrderBy = None) -> (Iterable[Task], int):
    """
    Получает список задач

    :param page: Страница
    :param order_by: Порядок сортировки
    :return: Список задач (Iterable[Task])
    """
    match TaskOrderBy(order_by):
        case TaskOrderBy.USERNAME:
            order_by = +Task.username
        case TaskOrderBy.USERNAME_DESC:
            order_by = -Task.username
        case TaskOrderBy.EMAIL:
            order_by = +Task.email
        case TaskOrderBy.EMAIL_DESC:
            order_by = -Task.email
        case TaskOrderBy.IS_COMPLETED:
            order_by = +Task.is_completed
        case TaskOrderBy.IS_COMPLETED_DESC:
            order_by = -Task.is_completed
        case _:
            order_by = None

    all_tasks = Task.select()
    all_tasks_count = all_tasks.count() or 0
    task_list = all_tasks.order_by(order_by).paginate(page, app.config['TASKS_ON_PAGE'])
    return task_list, all_tasks_count


def create_task(username: str, email: str, description: str) -> Task:
    """
    Создаёт задачу

    :param username: Имя пользователя
    :param email: E-Mail
    :param description: Описание задачи
    :return: Объект задачи (Task)
    """
    task = Task.create(
        username=username,
        email=email,
        description=description,
    )
    task.save()
    return task


def update_task(task_id: int, description: str, is_completed: bool):
    """
    Редактирует задачу

    P.S. Не будет работать, если использовать другую СУБД (напр. MySQL или PostgreSQL),
    потому что используется Raw SQL и символ '?' для обозначения параметров.
    С помощью данного символа параметры обозначаются в SQLite, в остальных используется '%s'.

    :param task_id: ID задачи, который нужно отредактировать
    :param description: Новое описание задачи
    :param is_completed: Выполнена задача или нет
    :return: True, если задача был отредактирована и False, если нет задачи с таким ID
    """
    query = Task.raw(
        f"""
            UPDATE {Task._meta.table_name}
                SET 
                {Task.description.column_name} = ?,
                {Task.is_completed.column_name} = ?,
                {Task.edited_by_administrator.column_name} = CASE
                    WHEN {Task.description.column_name} != ? THEN 1
                    ELSE {Task.edited_by_administrator.column_name}
                END
            WHERE id = ?;
        """,
        description,
        is_completed,
        description,
        task_id,
    )
    query.execute()


def auth_user(username: str, password: str) -> bool:
    """
    Проверяет данные пользователя

    :param username: Имя пользователя
    :param password: Пароль
    :return: Возвращает True, если имя пользователя и пароль соответствуют тем, что указаны в конфиге
    """
    return username == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PASSWORD']


def is_user_admin(username: str) -> bool:
    """
    Проверяет, является ли данный пользователь администратором

    :param username: Имя пользователя
    :return: True, если пользователь админ
    """
    return username == app.config['ADMIN_USERNAME']
