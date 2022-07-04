from sqlalchemy.orm import Session
from app.users.schemas import UserCreate, UserUpdateSchema
from app.core.hashing import Hasher
from datetime import datetime, timedelta
import os
from jose import jwt, JWTError
from typing import Union
from dotenv import load_dotenv
from app.users.models import User
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.authentication import JWTBearer, verify_token

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def check_is_exist(user: UserCreate, db: Session):
    print(user)
    is_exist = User.select().where(username=user.email)
    if is_exist:
        return True
    else:
        return False


def check_user(email: str, db: Session):
    if email:
        data_exist = db.query(User).filter(User.email == email).first()
        print(data_exist)
        if data_exist:
            return data_exist
    return None


def get_list_of_user(db: Session):
    data = db.query(User).all()
    return data


def get_user_detail(id: int, db: Session):
    data = db.query(User).filter(User.id == id).first()
    if data:
        return data
    else:
        return None


def update_user_by_id(id: int, user: UserUpdateSchema, db: Session):
    existing_job = db.query(User).filter(User.id == id)
    if not existing_job.first():
        return 0
    user.__dict__.update(
        username=user.username,
        is_active=user.is_active,
        is_superuser=user.is_superuser
    )  # update dictionary with new key values
    existing_job.update(user.__dict__)
    db.commit()
    return 1


def delete_user_by_id(id: int, db: Session):
    existing_job = db.query(User).filter(User.id == id)
    if not existing_job.first():
        return 0
    existing_job.delete(synchronize_session=False)
    db.commit()
    return 1


def authenticate_user(db: Session, email: str, password: str):
    user = check_user(email, db)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user


#
# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


def create_new_user(user: UserCreate, db: Session):
    user = User(username=user.username,
                email=user.email,
                hashed_password=Hasher.get_password_hash(user.password),
                is_active=True,
                is_superuser=False
                )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_access_token(data: dict):
    expires_delta = ACCESS_TOKEN_EXPIRE_MINUTES
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=int(expires_delta))
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    payload = {
        "email": data,
        "exp": expire
    }
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    refresh = create_refresh_token("Testing")
    payload = {
        "access_token": encoded_jwt,
        "refresh_token": refresh
    }
    return payload


def create_refresh_token(subject: Union[str, None], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=int(REFRESH_TOKEN_EXPIRE_MINUTES))

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print(token)

    return verify_token(token, credentials_exception)


