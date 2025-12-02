from uuid import UUID


class IdempotencyKey(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value, info=None):
        try:
            UUID(value)
        except Exception:
            raise ValueError("Idempotency-Key must be a valid UUID")
        return value
