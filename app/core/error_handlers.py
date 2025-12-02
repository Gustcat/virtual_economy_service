from http import HTTPStatus
from typing import Type

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AppError,
    UserNotFoundError,
    ProductNotFoundError,
    ProductInactiveError,
    InventoryAlreadyExistsError,
    InsufficientBalanceError,
    PermanentProductQuantityError,
    PermanentProductUseError,
    InsufficientProductQuantityError,
    IdempotencyKeyConflictError,
)

APP_ERROR_STATUS_MAP: dict[Type[AppError], HTTPStatus] = {
    UserNotFoundError: HTTPStatus.NOT_FOUND,
    ProductNotFoundError: HTTPStatus.NOT_FOUND,
    ProductInactiveError: HTTPStatus.CONFLICT,
    InventoryAlreadyExistsError: HTTPStatus.CONFLICT,
    InsufficientBalanceError: HTTPStatus.BAD_REQUEST,
    PermanentProductQuantityError: HTTPStatus.BAD_REQUEST,
    PermanentProductUseError: HTTPStatus.BAD_REQUEST,
    InsufficientProductQuantityError: HTTPStatus.CONFLICT,
    IdempotencyKeyConflictError: HTTPStatus.CONFLICT,
}


def register_errors_handlers(app: FastAPI) -> None:

    @app.exception_handler(AppError)
    def handle_app_error(request: Request, exc: AppError):
        status_code = APP_ERROR_STATUS_MAP.get(type(exc), 500)
        return JSONResponse(status_code=status_code, content={"error": str(exc)})
