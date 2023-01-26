import httpx
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(status_code=403, detail='Invalid authentication scheme.')

            isTokenValid = await self.verify_jwt(credentials.credentials)
            if not isTokenValid:
                raise HTTPException(status_code=401, detail='Invalid token or expired token.')
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail='Invalid authorization code.')

    async def verify_jwt(self, jwtoken: str) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                'http://nginx:80/v1/check_perm', headers={'Authorization': 'Bearer ' + jwtoken}
            )
        if response.status_code == 200:
            return True
        else:
            return False
