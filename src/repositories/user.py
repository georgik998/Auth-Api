from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union

from src.models.auth import RegistrationData

from src.infra.logi import logger


class __UserRepoPost:
    @staticmethod
    async def post(session: AsyncSession, data) -> int:
        query = await session.execute(text(
            'INSERT INTO users '
            '(phone_number,email,password,sex, full_name) '
            'VALUES(:phone_number,:email,:password,:sex,:full_name) '
            'RETURNING id;'),
            data)
        await session.commit()
        return query.scalar()

    @staticmethod
    async def update_password(session: AsyncSession, user_id: int, password: str):
        await session.execute(text('UPDATE users SET password = :password WHERE id = :user_id'),
                              {'user_id': user_id, 'password': password})
        await session.commit()


class __UserRepoGet:
    @staticmethod
    async def get_id_by_phone_number(session: AsyncSession, phone_number) -> Union[int, None]:
        query = await session.execute(text('SELECT id FROM users WHERE phone_number = :phone_number'), {
            'phone_number': phone_number
        })
        if query is None:
            return None
        return query.scalar_one_or_none()

    @staticmethod
    async def get_id_by_email(session: AsyncSession, email) -> Union[int, None]:
        query = await session.execute(text('SELECT id FROM users WHERE email = :email'), {
            'email': email
        })
        if query is None:
            return None
        return query.scalar_one_or_none()

    @staticmethod
    async def get_password_by_email(session: AsyncSession, email: str) -> Union[int, None]:
        query = await session.execute(text('SELECT  password FROM users WHERE email = :email'), {
            'email': email,
        })
        if query is None:
            return None
        return query.scalar_one_or_none()


class UserRepo(
    __UserRepoPost,
    __UserRepoGet
):
    def __init__(self):
        ...


user_repo = UserRepo()
