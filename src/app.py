from fastapi import FastAPI, APIRouter
from src.routers.token import router as token_router
from src.config import Config
from src.common.config import CommonConfig
from fastapi.middleware.cors import CORSMiddleware




def create_app():
    app = FastAPI(
        docs_url=None if CommonConfig.ENVIRONMENT == 'PRODUCTION' else "/docs",
        redoc_url=None if CommonConfig.ENVIRONMENT == 'PRODUCTION'  else "/redoc",
        openapi_url=None if CommonConfig.ENVIRONMENT == 'PRODUCTION'  else "/openapi.json"        
    )


    origins = CommonConfig.ALLOWED_ORIGINS

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # trusted origins
        allow_credentials=True,
        allow_methods=["*"],    # or restrict ["GET", "POST"]
        allow_headers=["*"],    # or restrict ["Authorization", "Content-Type"]
    )

    app.include_router(token_router)
    return app








