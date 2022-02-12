from fastapi import (
    APIRouter,
    Request,
)
from ..config import Config


router = APIRouter(prefix="/test")


@router.get("/component")
async def component(request: Request):
    config: Config = request.app.config
    return config.component
