from datetime import datetime

from peewee import *

from app import db


class Task(Model):
    id = AutoField()
    username = CharField(max_length=256, verbose_name='Имя пользователя', index=True)
    email = CharField(max_length=128, verbose_name='E-Mail', index=True)
    description = TextField(verbose_name='Текст задачи')
    is_completed = BooleanField(default=False, verbose_name='Задача выполнена')
    edited_by_administrator = BooleanField(default=False, verbose_name='Задача отредактирована администратором')
    created_at = DateTimeField(default=datetime.now, verbose_name='Дата создания')

    def __str__(self):
        return f'A task for {self.username} - f{"Done!" if self.is_completed else "Waiting..."}'

    class Meta:
        database = db
        table_name = 'tasks'


# Создаём таблицы
model_classes = Model.__subclasses__()
db.create_tables([*model_classes])
