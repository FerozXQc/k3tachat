import redis
from decouple import config
import secrets
from starlette.datastructures import MutableHeaders
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

r = redis.Redis.from_url(config('REDIS_URL'), decode_responses=True)
expiry = int(config('EXPIRY'))

def create_session(user:str):
    session = secrets.token_hex(20) 
    r.setex(f'session:{session}',expiry,user)
    return session

def get_user_from_session(session:str):
    return r.get(f'session:{session}')

def delete_session(session:str):
    return r.delete(f'session:{session}')
    
class refreshSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request:Request, call_next):
        if request.url.path == "/auth/logout":
            return await call_next(request)
        session = request.cookies.get('session')
        if session and r.exists(f'session:{session}'):
            user = r.get(f'session:{session}')
            r.setex(f'session:{session}',expiry,user)
            response = await call_next(request)
            response.set_cookie(
                key="session",
                value=session,
                httponly=True,
                max_age=expiry
            )
            return response
        else:
            return await call_next(request)