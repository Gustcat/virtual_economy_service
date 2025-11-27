from datetime import datetime
from enum import StrEnum

from sqlalchemy import func, String, ForeignKey, Integer, UniqueConstraint, Index, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)

    balance: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    inventory_items: Mapped[list["Inventory"]] = relationship(back_populates="user")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user")


class ProductType(StrEnum):
    CONSUMABLE = "consumable"
    PERMANENT = "permanent"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    description: Mapped[str | None]

    price: Mapped[int] = mapped_column(Integer, nullable=False)

    type: Mapped[ProductType] = mapped_column(
        Enum(ProductType, name="product_type", values_callable=lambda enum: [member.value for member in enum]),
        nullable=False,
    )

    is_active: Mapped[bool] = True

    __table_args__ = (
        Index(
            "idx_products_active",
            "id",
            postgresql_where=(is_active == True)
        ),
    )

    inventory_items: Mapped[list["Inventory"]] = relationship(back_populates="product")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="product")


class Inventory(Base):
    __tablename__ = "inventories"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)

    quantity: Mapped[int | None] = mapped_column(nullable=True)

    purchased_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="uix_user_product"),
    )

    user: Mapped["User"] = relationship(back_populates="inventory_items")
    product: Mapped["Product"] = relationship(back_populates="inventory_items")


class Status(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)

    amount: Mapped[int] = mapped_column(Integer, nullable=False)

    status: Mapped[str] = mapped_column(
        Enum(Status, name="status", values_callable=lambda enum: [member.value for member in enum]),
        index=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )

    __table_args__ = (
        Index("idx_transactions_product_created",
              "product_id",
              "created_at"),
    )

    user: Mapped["User"] = relationship(back_populates="transactions")
    product: Mapped["Product"] = relationship(back_populates="transactions")
