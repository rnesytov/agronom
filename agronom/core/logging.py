import json
import logging

from django.conf import settings


def filter_index(s):
    if s.startswith("@"):
        return False
    if s in ("geoip", "host", "message"):
        return False
    return True


def validate_extra_fields(func):
    def wrapper_validate_extra_fields(*args, **kwargs):
        extra = kwargs.get("extra", {})
        for field in extra:
            if field not in INDEXED_EXTRA_FIELDS:
                raise ValueError(
                    f"Field '{field}' is not indexed. "
                    f"Add it to {settings.ELASTIC_INDEX_FILE_PATH}"
                )
        func(*args, **kwargs)
    return wrapper_validate_extra_fields


class ELKLogger(logging.getLoggerClass()):

    debug = validate_extra_fields(logging.getLoggerClass().debug)
    info = validate_extra_fields(logging.getLoggerClass().info)
    warning = validate_extra_fields(logging.getLoggerClass().warning)
    warn = validate_extra_fields(logging.getLoggerClass().warn)
    error = validate_extra_fields(logging.getLoggerClass().error)
    exception = validate_extra_fields(logging.getLoggerClass().exception)
    critical = validate_extra_fields(logging.getLoggerClass().critical)
    fatal = validate_extra_fields(logging.getLoggerClass().fatal)


def getLogger(name):
    if name.startswith(f"{settings.PROJECT_NAME}."):
        return logging.getLogger(name)
    return logging.getLogger(f"{settings.PROJECT_NAME}." + name)


if not settings.PRODUCTION_MODE:
    with open(settings.ELASTIC_INDEX_FILE_PATH) as f:
        j = json.load(f)['mappings']["_default_"]["properties"]

        INDEXED_EXTRA_FIELDS = tuple(filter(filter_index, j))
    logging.setLoggerClass(ELKLogger)
