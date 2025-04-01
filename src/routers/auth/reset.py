from fastapi import APIRouter, Query

from src.models.auth import ResetPasswordData, NewPasswordData
from src.infra.database import async_session
from src.services.auth import auth_service

router = APIRouter()


@router.post('/reset-password')
async def reset_password(data: ResetPasswordData):
    async with async_session() as session:
        return await auth_service.start_reset_password(session, data)


@router.post('/check-reset-password-token')
async def check_reset_password_token(token: str = Query(alias='token')):
    return bool(await auth_service.check_reset_password_token(token))


@router.post('/new-password')
async def new_password(data: NewPasswordData):
    async with async_session() as session:
        return await auth_service.reset_password(session, data)
