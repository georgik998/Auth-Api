from fastapi import APIRouter

from src.models.auth import LoginData
from src.infra.database import async_session
from src.services.auth import auth_service

router = APIRouter()


@router.post('/login')
async def login(data: LoginData):
    async with async_session() as session:
        data = await auth_service.login(session=session, data=data)
    return data
