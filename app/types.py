from enum import Enum


class TaskOrderBy(Enum):
    USERNAME = 'username_asc'
    USERNAME_DESC = 'username_desc'
    EMAIL = 'email_asc'
    EMAIL_DESC = 'email_desc'
    IS_COMPLETED = 'isCompleted_asc'
    IS_COMPLETED_DESC = 'isCompleted_desc'
    NONE = 'null'
