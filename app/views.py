from flask import request
from flask_pydantic import validate
from pydantic import ValidationError

from app import app, schemas
from app.services import get_tasks, create_task, update_task, auth_user
from app.utils import for_admin_only, jwt_encode


@app.get('/tasks')
# @validate(query=schemas.GetTasks)
# def tasks_get(query: schemas.GetTasks):
def tasks_get():
    # По какой-то причине Flask-Pydantic не хочет работать конкретно с Query Params в данном случае.
    # Чтобы не тратить лишнее время - просто распарсил их самостоятельно.
    # P.S. Я вообще больше люблю Django, с Flask-Pydantic не работал до этого)
    try:
        query = schemas.GetTasks(**request.args.to_dict())
    except ValidationError as e:
        return e.json(), 400

    tasks, task_count = get_tasks(page=query.page, order_by=query.order_by)
    resp = schemas.Tasks(
        count=task_count or 0,
        items=[schemas.Task.model_validate(task) for task in tasks]
    ).model_dump_json(by_alias=True)
    return resp, 200


@app.post('/tasks')
@validate(response_by_alias=True, on_success_status=201)
def tasks_post(body: schemas.CreateTask):
    task = create_task(username=body.username, email=body.email, description=body.description)
    resp = schemas.Task.model_validate(task).model_dump_json(by_alias=True)
    return resp, 201


@app.put('/tasks/<int:task_id>')
@for_admin_only
@validate(response_by_alias=True)
def tasks_put(task_id: int, body: schemas.EditTask):
    update_task(task_id=task_id, description=body.description, is_completed=body.is_completed)
    resp = schemas.Ok().model_dump_json(by_alias=True)
    return resp, 200


@app.post('/auth')
@validate(response_by_alias=True)
def auth_post(body: schemas.LogIn):
    is_ok = auth_user(username=body.username, password=body.password)
    if is_ok:
        token = jwt_encode(username=body.username)
        resp = schemas.Token(token=token).model_dump_json(by_alias=True)
        return resp, 200
    else:
        resp = schemas.Error(detail='Invalid username or password!').model_dump_json(by_alias=True)
        return resp, 401
