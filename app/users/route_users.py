from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import status, Request, HTTPException
from app.users.schemas import UserCreate, UserLoginSchema, UserUpdateSchema, ShowUser
from app.db.session import get_db
from app.users.auth import (create_new_user, check_user, create_access_token, authenticate_user,
                            get_list_of_user, get_user_detail, update_user_by_id, delete_user_by_id)
from app.authentication import JWTBearer

router = APIRouter()


# pagination


@router.get("/")
def index():
    return {"Welcome Dear..!!"}


@router.post("/users/signup")
def user_signup(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    print(user)
    if user:
        jwt = create_access_token(user.email)
        data = {
            "id": user.id,
            "token": jwt,
            "email": user.email,
            "username": user.username,
            "is_active": user.is_active
        }
        return data
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Failed to signup",
    )


@router.post("/users/login")
def user_jwt_login(user: UserLoginSchema, db: Session = Depends(get_db), response_model=ShowUser):
    user = authenticate_user(db, user.email, user.password)
    if not user:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    jwt = create_access_token(data=user.email)
    data = {
        "id": user.id,
        "token": jwt,
        "email": user.email,
        "username": user.username
    }
    return data


@router.get("/users/getAllUsersList")
def get_all_users(db: Session = Depends(get_db)):
    users = get_list_of_user(db)
    data_list = list()
    if users:
        for use in users:
            data = {
                "id": use.id,
                "email": use.email,
                "username": use.username,
                "is_active": use.is_active,
                "is_superuser": use.is_superuser,
            }
            data_list.append(data)
        return data_list


@router.get("/users/getUserDetail/{id}")
def get_all_users(id: int, db: Session = Depends(get_db)):
    users = get_user_detail(id, db)
    if users:
        data = {
            "id": users.id,
            "email": users.email,
            "username": users.username,
            "is_active": users.is_active,
            "is_superuser": users.is_superuser,
        }
        return data
    else:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User does not exist",
        )


@router.patch("/users/updateUserDetail/{id}/")
def update_user_detail(id: int, user: UserUpdateSchema, db: Session = Depends(get_db)):
    message = update_user_by_id(id, user, db)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )
    return {"msg": "Successfully updated data."}


@router.delete("/users/deleteUser/{id}")
def delete_job(id: int, db: Session = Depends(get_db)):
    user_exist = get_user_detail(id=id, db=db)
    if not user_exist:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User does not exist",
        )
    if user_exist:
        delete_user_by_id(id=id, db=db)
        return {"detail": "User deleted Successfully."}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted!!!!"
    )
