class AppError(Exception):
    pass


class UserNotFoundError(AppError):
    def __init__(self, user_id: int):
        super().__init__(f"User with {user_id=} not found")


class ProductNotFoundError(AppError):
    def __init__(self, product_id: int):
        super().__init__(f"Product with {product_id=} not found")


class ProductInactiveError(AppError):
    def __init__(self, product_id: int):
        super().__init__(f"Product with {product_id=} is inactive")


class InventoryAlreadyExistsError(AppError):
    def __init__(self, product_id: int):
        super().__init__(f"Inventory with {product_id=} already exists")


class InsufficientBalanceError(AppError):
    def __init__(self, balance, total_cost: int):
        super().__init__(f"Insufficient {balance=} for {total_cost=}")


class PermanentProductQuantityError(AppError):
    def __init__(self):
        super().__init__("Cannot purchase more than one of a permanent product.")


class PermanentProductUseError(AppError):
    def __init__(self):
        super().__init__(f"Cannot use permanent product")


class InsufficientProductQuantityError(AppError):
    def __init__(self, available_q, requested_q: int):
        super().__init__(
            f"Insufficient product quantity: available {available_q}, requested {requested_q}"
        )


class IdempotencyKeyConflictError(AppError):
    def __init__(self):
        super().__init__("Idempotency key already used with different data")
