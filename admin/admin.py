from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, APIRouter, status, Header
from typing import Annotated
from jose import JWTError, jwt
from passlib.context import CryptContext

from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session


from db.models import User
from db.crud import get_user_by_name, create_user
from db.schemas import User, UserBase, UserCreate, Token, Userlogin
from dependencies import get_db, authenticate

# in productionsecret key must be in env variables
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user( user_id: str, password: str, db: Session):
    
    user = get_user_by_name(db=db, username=user_id)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/token")
async def login_for_access_token(user_model: Userlogin , db: Session = Depends(get_db)):
    user = authenticate_user(user_model.username, user_model.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/createuser")
async def create_new_user(new_user : UserCreate, token: Annotated[str, Header()], db: Session = Depends(get_db)):
    authenticate(token)
    hashed_password = get_password_hash(new_user.password)
    new_user.password = hashed_password
    user = create_user(db=db, user=new_user)
    return user