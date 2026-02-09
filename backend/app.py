from fastapi import FastAPI

def create_app():
    app = FastAPI(title="Secure Cloud Blockchain AI")

    from backend.routes.health import router as health_router
    from backend.routes.upload import router as upload_router

    app.include_router(health_router, prefix="/health", tags=["Health"])
    app.include_router(upload_router, prefix="/upload", tags=["Upload"])

    return app

app = create_app()