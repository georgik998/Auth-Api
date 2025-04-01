from pydantic_settings import BaseSettings


class ApiSettings(BaseSettings):
    API_DOCS_URL: str
    API_HOST: str
    API_PORT: int

    BASE_PREFIX: str = ''
    TITLE: str = 'BuziakDating main api server'
    DESCRIPTION: str = """
Main api microservice for buziak dating

**No compute service, default api endpoints + logic**
"""

    class Config:
        env_file = "src/.env"
        extra = "allow"


class JwtSettings(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_KEY: str = 'access-token'
    REFRESH_TOKEN_KEY: str = 'refresh-token'

    ACCESS_TOKEN_EXPIRE: int = 1 * 60 * 60  # 1 час
    REFRESH_TOKEN_EXPIRE: int = 30 * 24 * 60 * 60  # 30 дней

    class Config:
        env_file = "src/.env"
        extra = "allow"




jwt_settings = JwtSettings()

api_settings = ApiSettings()
