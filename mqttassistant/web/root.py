from fastapi import Request


async def home(request: Request):
    return request.app.templates.TemplateResponse('home.html', dict(request=request))
