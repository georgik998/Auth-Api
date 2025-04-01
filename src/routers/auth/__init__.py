from fastapi import APIRouter

from src.routers.auth.registration import router as registr_router
from src.routers.auth.login import router as login_router
from src.routers.auth.reset import router as reset_router

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

router.include_router(registr_router)
router.include_router(login_router)
router.include_router(reset_router)
