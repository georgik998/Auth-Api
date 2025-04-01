from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from src.infra.database.settings import postgresql_settings
from sqlalchemy import text

user = postgresql_settings.POSTGRES_USER
password = postgresql_settings.POSTGRES_PASSWORD
host = postgresql_settings.POSTGRES_HOST
port = postgresql_settings.POSTGRES_PORT
dbname = postgresql_settings.POSTGRES_DB

DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=50,
    max_overflow=5,
)

async_session = async_sessionmaker(
    engine, expire_on_commit=False,
)


async def test_driver():
    async with async_session() as session:
        async with session.begin():
            await session.execute(text('SELECT 1;'))
