LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s | <%(name)s> [%(levelname)s]: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": "logs/app.log",
            "maxBytes": 1024 * 1024,
            "backupCount": 1,
            "encoding": "utf-8",
            "level": "DEBUG",
        },
    },
    "root": {
        "handlers": ["file", "console"],
        "level": "DEBUG",
    },
}
