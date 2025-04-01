from fastapi import APIRouter, Cookie, Response

from src.infra.database import async_session

from src.models.auth import RegistrationData, ConfirmCodeData
from src.services.auth import auth_service
from src.config import jwt_settings

router = APIRouter()


@router.post('/registration',
             description="""Возвращаем либо uuid для посадки в куку, для дальнейшей проверки кода подтверждения регистрации,
              
             либо получаем сообщение о уже зарегистрированом юзере
             
             Время жизни кода - 5 минут""")
async def register(data: RegistrationData):
    async with async_session() as session:
        data = await auth_service.check_registration_availability(
            data=data,
            session=session
        )
    return data


@router.post('/confirm-code')
async def confirm_code(response: Response, data: ConfirmCodeData):
    async with async_session() as session:
        data = await auth_service.check_registration_code(session=session, data=data)
    if data['status'] == 'ok':
        response.set_cookie(
            key=jwt_settings.REFRESH_TOKEN_KEY,
            value=data['data']['refresh-token'],
            secure=True,
            httponly=True,
            samesite="strict",
            max_age=jwt_settings.REFRESH_TOKEN_EXPIRE
        )
    return data
