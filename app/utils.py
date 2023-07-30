from datetime import timedelta, datetime
from typing import Callable

import jwt
from flask import request, jsonify
from loguru import logger

from app import app
from app.services import is_user_admin


def jwt_encode(username: str) -> str:
    token = jwt.encode({
        'username': username,
        'exp': datetime.utcnow() + timedelta(days=365),
    }, app.config['SECRET_KEY'], algorithm="HS256")
    return token


def jwt_decode(token: str) -> dict[str]:
    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    return data


def for_admin_only(func: Callable) -> Callable:
    """
    Декоратор позволяет пользоваться роутом только администратору
    """

    def wrapper(*args, **kwargs):
        # Получаем токен
        token = request.headers.get('x-access-token')

        # Токена нет, возвращаем 401
        if token is None:
            return jsonify({'message': 'Token is missing!'}), 401

        # Получаем данные из токена
        try:
            data = jwt_decode(token)
        except (jwt.PyJWTError, TypeError, ValueError) as e:
            logger.exception(e)
            return jsonify({'message': 'Invalid token!'}), 401

        # Проверяем, является ли пользователь администратором
        if not is_user_admin(username=data['username']):
            return jsonify({'message': 'Forbidden!'}), 403

        return func(*args, **kwargs)

    return wrapper


def pydantic_validate(func: Callable) -> Callable:
    """
    Декоратор позволяет валидировать
    """

    def wrapper(*args, **kwargs):
        # Получаем токен
        token = request.headers.get('x-access-token')

        # Токена нет, возвращаем 401
        if token is None:
            return jsonify({'message': 'Token is missing!'}), 401

        # Получаем данные из токена
        try:
            data = jwt_decode(token)
        except (jwt.PyJWTError, TypeError, ValueError) as e:
            logger.exception(e)
            return jsonify({'message': 'Invalid token!'}), 401

        # Проверяем, является ли пользователь администратором
        if not is_user_admin(username=data['username']):
            return jsonify({'message': 'Forbidden!'}), 403

        return func(*args, **kwargs)

    return wrapper
