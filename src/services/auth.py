from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union, List, Optional
from uuid import uuid4
from random import randint

from src.infra.logi import logger
from src.infra.email_client import email_client
from src.infra.redis import redis_repo

from src.repositories.user import user_repo, UserRepo

from src.models.auth import RegistrationData, ConfirmCodeData, JwtTokenType, LoginData, ResetPasswordData, \
    NewPasswordData

from src.utils.answers import build_default_answer

from src.utils.security import security_utils


class AuthService:
    __user_repo: UserRepo = user_repo

    @staticmethod
    async def start_registration(data: RegistrationData):
        registration_code_key = str(uuid4())
        code = str(randint(10_000, 99_999))
        user_data = data.model_dump()
        user_data.update({
            'email_code': code
        })
        user_data['sex'] = user_data['sex'].value
        await redis_repo.set_cache(
            name=f'code={registration_code_key}',
            value=user_data,
            expire=5 * 60
        )
        email_client.send_email(
            receiver_email=user_data['email'],
            title='Код подтверждения регистрации',
            body=f'Ваш код: {code}'
        )
        return registration_code_key

    async def check_registration_availability(self, data: RegistrationData, session: AsyncSession):
        phone_number_availability = await self.__user_repo.get_id_by_phone_number(session=session,
                                                                                  phone_number=data.phone_number)
        email_availability = await self.__user_repo.get_id_by_email(session=session,
                                                                    email=data.email)
        await session.close()
        if not phone_number_availability and not email_availability:
            registration_code_key = await self.start_registration(data)
            return build_default_answer(
                data={'code_id': registration_code_key, }
            )
        return build_default_answer(
            status=False,
            data={
                'email_availability': bool(email_availability),
                'phone_number_availability': bool(phone_number_availability)
            }
        )

    async def check_registration_code(self, session: AsyncSession, data: ConfirmCodeData):
        code = data.code
        user_data = await redis_repo.get_cache(f'code={data.registration_code_key}')
        if not user_data:
            return build_default_answer(
                status=False,
                message='Code expire'
            )
        true_code = user_data['email_code']
        if true_code != code:
            return build_default_answer(
                status=False,
                message='Code incorrect'
            )
        await redis_repo.delete_cache(f'code={data.registration_code_key}')

        user_data['password'] = security_utils.hash_password(user_data['password'])
        user_id = await self.__user_repo.post(session=session, data=user_data)
        jwt_payload = {
            'user_id': user_id,
        }
        access_token = security_utils.create_token(payload=jwt_payload, token_type=JwtTokenType.access)
        refresh_token = security_utils.create_token(payload=jwt_payload, token_type=JwtTokenType.refresh)
        return build_default_answer(data={'access-token': access_token, 'refresh-token': refresh_token})

    async def login(self, session: AsyncSession, data: LoginData):
        user_id = await self.__user_repo.get_id_by_email(session, data.email)
        if user_id is None:
            return build_default_answer(
                status=True,
                message='Login is incorrect',
                data=None
            )
        hashed_password = await self.__user_repo.get_password_by_email(session=session, email=data.email)
        if not security_utils.check_password(password=data.password, hashed_password=hashed_password):
            return build_default_answer(
                status=True,
                message='Password is incorrect',
                data=None
            )
        access_token = security_utils.create_token(payload={'user_id': user_id}, token_type=JwtTokenType.access)
        return build_default_answer(
            status=True,
            message='Login success',
            data={
                'access-token': access_token
            }
        )

    async def start_reset_password(self, session: AsyncSession, data: ResetPasswordData):
        user_id = await self.__user_repo.get_id_by_email(session, data.email)
        if user_id is None:
            return build_default_answer(
                status=False,
                message='Login is incorrect',
                data=None
            )

        reset_password_token = str(uuid4())
        await redis_repo.set_cache(
            name=f'reset_code={reset_password_token}',
            value=user_id,
            expire=10 * 60
        )
        email_client.send_email(
            receiver_email=data.email,
            title='Сброс пароля',
            body=f'Ваша ссылка для сброса пароля: http://localhost:6543/auth/new-password?token={reset_password_token}')
        return build_default_answer()

    @staticmethod
    async def check_reset_password_token(token: str):
        user_id = await redis_repo.get_cache(f'reset_code={token}')
        if not user_id:
            return False
        return user_id

    async def reset_password(self, session: AsyncSession, data: NewPasswordData):
        user_id = await self.check_reset_password_token(token=data.token)
        if not user_id:
            return False
        await redis_repo.delete_cache(f'reset_code={data.token}')
        await self.__user_repo.update_password(session=session, user_id=user_id,
                                               password=security_utils.hash_password(data.password))
        return True


auth_service = AuthService()
