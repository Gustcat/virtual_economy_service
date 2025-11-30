import logging

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.db.session import SessionDep
from app.schemas.analytic import PopularProductSchema
from app.services.analytic import AnalyticService

analytic_router = APIRouter()
logger = logging.getLogger(__name__)


@analytic_router.get("/popular-products/", response_model=list[PopularProductSchema])
@cache(expire=3600)
async def list_popular_products(session: SessionDep):
    analytic_service = AnalyticService(session)
    popular_products = await analytic_service.list_popular_products()

    logger.debug(f"Get popular products: {popular_products}")
    return popular_products
