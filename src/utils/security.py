from bcrypt import checkpw, hashpw, gensalt
from jwt import decode, encode, ExpiredSignatureError, InvalidTokenError
from src.models.auth import JwtTokenType

from src.config import jwt_settings
from src.infra.logi import logger

class SecurityUtils:
    def __init__(self, jwt_secret, jwt_algorithm, jwt_access_expire, jwt_refresh_expire):
        self.__jwt_secret = jwt_secret
        self.__jwt_algorithm = jwt_algorithm
        self.__access_expire = jwt_access_expire
        self.__refresh_expire = jwt_refresh_expire

    @staticmethod
    def hash_password(password: str) -> str:
        return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    @staticmethod
    def check_password(password: str,
                       hashed_password):
        return checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def decode_token(self,
                     token: str):
        try:
            decoded_payload = decode(
                token,
                self.__jwt_secret,
                algorithms=[self.__jwt_algorithm]
            )
            token, status = decoded_payload, 'ok'
        except ExpiredSignatureError:
            token, status = None, "expired"
        except InvalidTokenError:
            token, status = None, "invalid"
        return {
            'token': token,
            'status': status
        }

    def create_token(self,
                     payload: dict,
                     token_type: JwtTokenType) -> str:
        token_type = token_type.value
        match token_type:
            case 'access':
                exp = self.__access_expire
            case 'refresh':
                exp = self.__refresh_expire
        payload['exp'] = exp
        return encode(
            payload,
            self.__jwt_secret,
            algorithm=self.__jwt_algorithm)

    def auth(self, access_token, refresh_token) -> dict:
        token_info = self.decode_token(access_token)
        if token_info['token'] is not None:
            return {
                'status': 'ok',
                'message': 'auth success',
                'data': {
                    'payload': token_info['token']
                }
            }
        token_info = self.decode_token(refresh_token)
        if token_info['token'] is None:
            return {
                'status': 'error',
                'message': 'access and refresh tokens expired or invalid, please login or register',
                'data': None
            }
        payload = token_info['token']
        access_token = self.create_token(payload, JwtTokenType.access)
        return {
            'status': 'ok',
            'message': 'access token updated',
            'data': {
                'access-token': access_token,
            }
        }


security_utils = SecurityUtils(
    jwt_secret=jwt_settings.JWT_SECRET,
    jwt_algorithm=jwt_settings.JWT_ALGORITHM,
    jwt_access_expire=jwt_settings.ACCESS_TOKEN_EXPIRE,
    jwt_refresh_expire=jwt_settings.REFRESH_TOKEN_EXPIRE
)

from fastapi import Header, Cookie
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException


def auth_user(Authorization: str = Header(), refresh_token: str = Cookie()):
    if not Authorization.startswith('Bearer '):
        raise HTTPException(
            status_code=400,
            detail='Access token format invalid, it must be: "Bearer <access-token>"'
        )
    auth_info = security_utils.auth(access_token=Authorization[len('Bearer '):], refresh_token=refresh_token)
    if auth_info['status'] != 'ok':
        raise HTTPException(
            status_code=401,
            detail=auth_info['message']

        )
    elif auth_info['data'].get('access-token'):
        return JSONResponse(
            status_code=200,
            content={
                'status': 'ok',
                'message': 'To continue need update new access token',
                'data': {
                    'access-token': auth_info['data']['access-token'],
                }
            }
        )
    return auth_info['data']['payload']
