# phase_wrapper.py

import time
import random
import asyncio
import functools
import logging
import json
from typing import Callable, Optional, Tuple, Union, Any

# Logging configuration
logger = logging.getLogger("phase_drift")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("phase_drift_log.json")
handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(handler)


def log_response(data: dict):
    logger.info(json.dumps(data))


def phase_wrap(
    delay_range: Tuple[float, float] = (0.8, 2.0),
    timeout: float = 10.0,
    fallback_message: Optional[Union[str, Callable[[], str]]] = "(…continued silence)",
):
    """
    Decorator to inject Phase Drift's core concepts into function calls.
    Applies a randomized delay, handles timeouts with fallback,
    and logs response characteristics in JSON format.
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            delay = random.uniform(*delay_range)
            start_time = time.time()
            await asyncio.sleep(delay)

            response_data = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "delay_seconds": delay,
                "timeout_seconds": timeout,
                "silence_used": False,
                "elapsed_time": None
            }

            try:
                result = await asyncio.wait_for(func(*args, **kwargs), timeout=timeout)
                response_data["elapsed_time"] = time.time() - start_time
                log_response(response_data)
                return result
            except asyncio.TimeoutError:
                response_data["silence_used"] = True
                response_data["elapsed_time"] = time.time() - start_time
                log_response(response_data)
                if callable(fallback_message):
                    return fallback_message()
                return fallback_message

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            delay = random.uniform(*delay_range)
            start_time = time.time()
            time.sleep(delay)

            response_data = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "delay_seconds": delay,
                "timeout_seconds": timeout,
                "silence_used": False,
                "elapsed_time": None
            }

            try:
                result = func(*args, **kwargs)
                response_data["elapsed_time"] = time.time() - start_time
                log_response(response_data)
                return result
            except Exception:
                # General functions do not support asyncio.TimeoutError; fallback on exception
                response_data["silence_used"] = True
                response_data["elapsed_time"] = time.time() - start_time
                log_response(response_data)
                if callable(fallback_message):
                    return fallback_message()
                return fallback_message

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator
