import time
import sentry_sdk


from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.responses import HTMLResponse
from redis import asyncio as aioredis
from sqladmin import Admin, ModelView
from fastapi_versioning import VersionedFastAPI, version

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.rooms.router import router as router_hotels_and_rooms
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.users.router import router as router_users
from app.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код для инициализации Redis и кэширования
    redis = aioredis.from_url(
        url=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    # Выход из приложения (закрытие соединений, очистка ресурсов)
    yield
    await redis.close()


app = FastAPI(lifespan=lifespan)

app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
)

print("---- Запуск FastAPI ----")

sentry_sdk.init(
    dsn="https://ad0ae478eb1b67930830c83892c2bfef@o4508987691302912.ingest.de.sentry.io/4508987696218192",
    send_default_pii=True,
)



admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)


app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels_and_rooms)
app.include_router(router_pages)
app.include_router(router_images)


origins = [
    "*",
]

"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)
"""

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # При подключении Prometheus + Grafana подобный лог не требуется
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })
    return response
