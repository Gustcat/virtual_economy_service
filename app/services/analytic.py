from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.product import ProductRepository
from app.schemas.analytic import PopularProductSchema


class AnalyticService:
    def __init__(self, session: AsyncSession):
        self.product_repo = ProductRepository(session)
        self.session = session

    async def list_popular_products(self) -> list[PopularProductSchema]:
        rows = await self.product_repo.list_popular_products()

        return [
            PopularProductSchema(
                id=product.id,
                name=product.name,
                description=product.description,
                type=product.type,
                purchase_count=purchase_count,
            )
            for product, purchase_count in rows
        ]
