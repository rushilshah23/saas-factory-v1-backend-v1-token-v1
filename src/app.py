from fastapi import FastAPI, APIRouter
from src.routers.token import router as token_router
from src.config import Config
from src.common.config import CommonConfig

def create_app():
    app = FastAPI(
        docs_url=None if CommonConfig.ENVIRONMENT == 'PRODUCTION' else "/docs",
        redoc_url=None if CommonConfig.ENVIRONMENT == 'PRODUCTION'  else "/redoc",
        openapi_url=None if CommonConfig.ENVIRONMENT == 'PRODUCTION'  else "/openapi.json"        
    )
    app.include_router(token_router)
    return app








