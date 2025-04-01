__all__ = ['http_client', 'HttpClient']

from typing import Union, Optional

from aiohttp import ClientSession, ClientResponse, ClientError, ClientTimeout
from asyncio import TimeoutError


class HttpClient:
    session: Optional[ClientSession] = None
    timeout = ClientTimeout(total=30)
    __allowed_methods = ['get', 'post', 'delete', 'put']

    def __init__(self):
        self.session = None

    async def create_session(self):
        if self.session is None or self.session.closed:
            self.session = ClientSession()

    async def close_session(self):
        if self.session and not self.session.closed:
            await self.session.close()

    async def fetch(
            self,
            url: str,
            method: str,
            json: Optional[dict] = None,
            params: Optional[dict] = None,
            headers: Optional[dict] = None
    ) -> Union[any, None]:
        assert method in self.__allowed_methods, 'request method not allowed'
        await self.create_session()
        try:
            async with self.session.request(
                    method=method,
                    url=url,
                    json=json,
                    params=params,
                    headers=headers,
                    timeout=self.timeout
            ) as response:
                try:
                    return await response.json()
                except Exception:
                    logger.warning(f"[PARSE JSON ERROR]  url={url} status={response.status}")
                    return None
        except (ClientError, TimeoutError) as e:
            logger.warning(f'[HTTP ERROR] url={url} [{e}]')
            return None


http_client = HttpClient()
