from datetime import datetime, timedelta

from sqlalchemy import select, func

from app.core.config import settings
from app.db.models import Product, Transaction


class ProductRepository:
    def __init__(self, session):
        self.session = session

    async def get_product(self, product_id: int) -> Product:
        stmt = select(Product).where(Product.id == product_id)
        result = await self.session.execute(stmt)
        product = result.scalar_one_or_none()
        return product

    async def list_popular_products(self,
                                    days: int = settings.days_for_product_top,
                                    limit: int = settings.amount_products_top) -> list[tuple[Product, int]]:
        actual_time_point = datetime.utcnow() - timedelta(days=days)

        stmt = (
            select(
                Product,
                func.count(Transaction.id).label("purchase_count"),
            )
            .join(Transaction, Transaction.product_id == Product.id)
            .where(
                Transaction.created_at >= actual_time_point,
                Transaction.status == "completed",
                Product.is_active == True,
            )
            .group_by(Product.id)
            .order_by(func.count(Transaction.id).desc())
            .limit(limit)
        )

        result = await self.session.execute(stmt)
        return result.all()
