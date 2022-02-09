from fastapi import Request, status, HTTPException
from .auth import Auth, User

async def home(request: Request):
    return request.app.templates.TemplateResponse('home.html', dict(request=request))


async def login(request: Request, user: User):
    user_verified = request.app.auth.authenticate(user.username, user.password)
    if not user_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = request.app.auth.get_token(user_verified)
    return dict(token=token)
    