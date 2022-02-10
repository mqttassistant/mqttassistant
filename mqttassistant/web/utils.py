from fastapi.security import OAuth2PasswordBearer
from fastapi import Request, Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_user(users, username):
    for user in users:
        if user.username == username:
            return user
    return False

async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    auth = request.app.config.auth
    username = auth.decode_token(token)
    return await get_user(request.app.config.users, username)

    