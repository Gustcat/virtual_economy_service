from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user import UserRepository


class UserService:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)
        self.session = session

    async def add_funds(self, user_id, amount: int) -> int:
        balance = await self.user_repo.add_funds(user_id, amount)
        await self.session.commit()
        return balance
