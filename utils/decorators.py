import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        response = func(*args, **kwargs)
        end = time.time()
        logger.info(f"Executed {func.__name__!r} in {end - start:.4f} seconds")
        return response
    return wrapper