from pydantic import BaseModel,EmailStr

class registerUserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

class loginUserSchema(BaseModel):
    username: str
    password: str

