from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound

from app.core.exceptions import UserNotFoundError
from app.db.models import User


class UserRepository:
    def __init__(self, session):
        self.session = session

    async def get_user(self, user_id: int, for_update: bool = False) -> User:
        stmt = select(User).where(User.id == user_id)
        if for_update:
            stmt = stmt.with_for_update()
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def add_funds(self, user_id, amount: int) -> int:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(balance=User.balance + amount)
            .returning(User.balance)
        )
        result = await self.session.execute(stmt)

        try:
            return result.scalar_one()
        except NoResultFound:
            raise UserNotFoundError(user_id)

    async def change_balance(self, user: User, new_balance: int) -> User:
        user.balance = new_balance
        self.session.add(user)
        await self.session.flush()
        return user
