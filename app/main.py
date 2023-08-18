from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.api.routers import main_router
from app.core.config import settings
from app.core.init_db import create_first_superuser

app = FastAPI(title=settings.app_title)

app.include_router(main_router)


@app.on_event('startup')
async def startup():
    """
    При старте приложения
    запускаем корутину create_first_superuser,
    отработает, если нет ни одного суперюзера
    """
    await create_first_superuser()


@app.api_route('/')
def main_redirect():
    return RedirectResponse('/docs')
