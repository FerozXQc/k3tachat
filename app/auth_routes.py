from fastapi import APIRouter, Response, Cookie, Request, HTTPException, Depends
from crud import db_check_user, db_create_user, verify_hash
from schemas import loginUserSchema, registerUserSchema
from redis_client import create_session, get_user_from_session, delete_session
from database import get_db,SessionLocal
from decouple import config

auth_router = APIRouter(tags=["auth"])

@auth_router.post('/login')
def loginUser(user:loginUserSchema, response:Response, db:SessionLocal = Depends(get_db)):
    db_user = db_check_user(user.username, db)
    if not db_user:
        return {'message': f'No user found with the username {username}'}
    if not verify_hash(db_user.password, user.password):
        return {'message': f'Invalid Password. try again!'}
    session = create_session(user.username)
    response.set_cookie(key='session', value=session, httponly=True, max_age=int(config('EXPIRY')))
    return {'message': 'login successful'}

@auth_router.post('/register')
def registerUser(user:registerUserSchema, db:SessionLocal = Depends(get_db)):

    if db_check_user(user.username, db):
        return {'message': f'user {user.username} is already taken.'}
    return db_create_user(user,db)

@auth_router.get('/me')
def me(session: str = Cookie(None)):
    if not session:
        raise HTTPException(status_code=403, detail="login expired/unauthorized")
    username = get_user_from_session(session)
    if username:
        return {"username": username}
    raise HTTPException(status_code=403, detail="login expired/unauthorized")

@auth_router.post("/logout")
def logout(response: Response, request: Request):
    session = request.cookies.get("session")
    if session:
        delete_session(session)
        response.delete_cookie("session")
    return {"message": "logged out"}