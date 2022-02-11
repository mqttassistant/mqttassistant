from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import (
    Optional,
)
from pydantic import (
    BaseModel,
    Extra,
)

class User(BaseModel):
    username: str = None
    password: str = None

class Auth(BaseModel):
    secret_key: Optional[str] = ''
    algorithm: Optional[str] = 'HS256'
    access_token_expire_minutes: Optional[int] = 30
    _pwd_context: None

    def __init__(self, *arg,**kwargs):
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        super().__init__(*arg,**kwargs)

    class Config:
        underscore_attrs_are_private = True
        extra=Extra.forbid

    def authenticate(self, user: User, plain_password):
        if not self.verify_password(plain_password, user.password):
            return False
        return user

    def verify_password(self, plain_password, hashed_password) -> bool:
        return self._pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str):
        return self._pwd_context.hash(password)

    def encode_token(self, user: User):
        to_encode = dict(username=user.username)
        expire = datetime.utcnow() + timedelta(self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> str:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("username")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        return username

