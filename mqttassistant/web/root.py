from fastapi import Request, status, HTTPException, Depends

from ..auth import  User
from .utils import get_current_user, get_user


async def home(request: Request, current_user: User = Depends(get_current_user)):
    return request.app.templates.TemplateResponse('home.html', dict(request=request))


async def login(request: Request, user_form: User):
    e = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    users = request.app.config.users
    auth = request.app.config.auth
    db_user = await get_user(users, user_form.username)
    if not db_user:
        raise e
    user_verified = auth.authenticate(db_user, user_form.password)
    if not user_verified:
        raise e
    token = auth.encode_token(user_verified)
    return dict(token=token)
