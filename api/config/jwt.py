import jwt
from fastapi import Header, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta

security = HTTPBearer()

class JwtAuth:
    def __init__(self):
        self.__secret = 'SECRET'

    def encode_token(self, user_id: str):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=50),
            'iat': datetime.utcnow(),
            'sub': user_id,
            'online': True
        }
        return jwt.encode(
            payload,
            self.__secret,
            algorithm='HS256'
        )

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, self.__secret, algorithms=['HS256'])
            if payload['online']:
                return payload['sub']
            else:
                raise  HTTPException(status_code=401, detail='Token enviado já inspirou. Realizar login novamente.')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token enviado já inspirou. Realizar login novamente.')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Token enviado é invalido. Realizar login novamente.')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)

    def logout(self, token: str):
        try:
            payload = jwt.decode(token, self.__secret, algorithms=['HS256'])
            payload['online'] = False
            return jwt.encode(
                payload,
                self.__secret,
                algorithm='HS256'
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token enviado já inspirou. Realizar login novamente.')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Token enviado é invalido. Realizar login novamente.')

    async def verify_token(self, token: str = Header('token')):
        return True
