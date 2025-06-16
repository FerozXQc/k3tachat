from database import get_db
from schemas import loginUserSchema, registerUserSchema
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError
from sqlalchemy.exc import IntegrityError
from models import User
from email_validator import validate_email, EmailNotValidError
ph = PasswordHasher(
    time_cost=3,
    memory_cost=131072,
    parallelism=4,
    hash_len=32,
    salt_len=16,
)


def verify_hash(hashed_password:str,password:str)-> bool: 
    if ph.verify(hashed_password,password):
        return True
    else:
        return False


def db_check_user(username:str, db)-> bool: 
    user = db.query(User).filter_by(username=username).first()
    if user:
        return user
    else:
        return False

def db_create_user(user:registerUserSchema,db):
    hashed_password = ph.hash(user.password)
    try:
        db.add(User(username=user.username, email=user.email, password = hashed_password))
        db.commit()
        return {'message': 'user created successfully.'}

    except IntegrityError as e:
        db.rollback()
        return {'message': f'error: {e}'}

