from typing import Optional
from pydantic import BaseModel,EmailStr

#properties required during user creation
class UserCreate(BaseModel):
    username: str
    email : EmailStr
    password : str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "abdulazeez@x.com",
                "password": "weakpassword"
            }
        }


class UserUpdateSchema(BaseModel):
    username: str
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    id : int
    username: str
    email: str
    is_active: bool
    is_superuser:bool

    class Config:  # to convert non dict obj to json
        orm_mode = True

class TokenData(BaseModel):
    email: EmailStr