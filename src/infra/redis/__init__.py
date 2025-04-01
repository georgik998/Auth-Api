import json
from typing import Any
from redis.asyncio import Redis

from src.infra.redis.config import redis_settings


class RedisRepository:

    def __init__(self, host, port):
        self.redis = Redis(
            host=host,
            port=port,
        )

    async def set_cache(self, name: str, value: Any, expire: int = 900) -> None:
        """
        Создание кэша.

        :param name: Имя кэша
        :param value: Значение кэша
        :param expire: время жизни кеша в секундах
        """
        serialized_data = json.dumps(value)
        return await self.redis.set(name=name, value=serialized_data, ex=expire)

    async def get_cache(self, name: str) -> Any:
        """
        Получение кэша.

        :param name: Имя кэша
        :return: Значение кэша
        """
        cache = await self.redis.get(name)
        if cache:
            return json.loads(cache)

    async def delete_cache(self, name: str) -> Any:
        """
        Удаление кэша.

        :param name: Имя кэша
        :return: None
        """
        if await self.get_cache(name):
            return await self.redis.delete(name)


redis_repo = RedisRepository(
    host=redis_settings.REDIS_HOST,
    port=redis_settings.REDIS_PORT
)
