from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    mail: Optional[str] = None
    full_name: Optional[str] = None

class Auth:
    users: Optional[dict] = dict()
    secret_key: Optional[str] = None
    algorithm: Optional[str] = None
    access_token_expire_minutes: Optional[int] = 30
    _pwd_context: None

    def __init__(self, users=dict(), secret_key='', algorithm='HS256', access_token_expire_minutes=30):
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.users = users
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes

    def authenticate(self, username, plain_password):
        user = self.get_user(username)
        if not user or not self.verify_password(plain_password, user.password):
            return False
        return user

    def get_user(self, username):
        if username in self.users:
            return User(**self.users[username])
        return False

    def verify_password(self, plain_password, hashed_password) -> bool:
        return self._pwd_context.verify(plain_password, hashed_password)

    def get_token(self, user: User):
        to_encode = dict(username=user.username)
        expire = datetime.utcnow() + timedelta(self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

