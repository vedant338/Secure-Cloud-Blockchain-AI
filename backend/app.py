from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger("backend")

def create_app():
    app = FastAPI(title="GUPTALAYA BLOCKSTORE")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from backend.routes.upload import router as upload_router
    from backend.routes.download import router as download_router
    from backend.routes.health import router as health_router
    from backend.routes.auth import router as auth_router

    app.include_router(upload_router, prefix="/upload")
    app.include_router(download_router, prefix="/download")
    app.include_router(health_router, prefix="/health")
    app.include_router(auth_router)

    logger.info("Backend application started")

    return app

app = create_app()