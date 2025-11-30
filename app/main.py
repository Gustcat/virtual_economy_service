from fastapi import FastAPI
import uvicorn

from app.api.v1.endpoints.analytics import analytic_router
from app.api.v1.endpoints.products import product_router
from app.api.v1.endpoints.users import user_router
from app.core.config import settings
from app.core.error_handlers import register_errors_handlers
from app.create_fastapi_app import lifespan

app = FastAPI(lifespan=lifespan)

register_errors_handlers(app)

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(product_router, prefix="/products", tags=["products"])
app.include_router(analytic_router, prefix="/analytics", tags=["analytics"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=settings.http_host, port=settings.http_port, reload=True
    )
