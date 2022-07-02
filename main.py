# import uvicorn
#
# if __name__ == "__main__":
#     uvicorn.run("app.api:app", host="0.0.0.0", port=8001, reload=True)
#

# main.py

from fastapi import FastAPI
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
from app.db.utils import check_db_connected, check_db_disconnected
from app.apis.base import api_router


def include_router(app):
    app.include_router(api_router)


def create_tables():
    print("create_tables")
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    create_tables()
    return app


app = start_application()


@app.on_event("startup")
async def app_startup():
    await check_db_connected()


@app.on_event("shutdown")
async def app_shutdown():
    await check_db_disconnected()
