import asyncio
import random
from typing import Callable, Any


def ThrottlingLimitError(error_message: str) -> bool:
    if not error_message:
        return False

    msg = str(error_message).lower()
    tokens = [
        "429",
        "rate limit",
        "rate_limit",
        "too many requests",
        "throttl",
        "resource_exhausted",
        "resource exhausted",
        "quota",
    ]
    return any(token in msg for token in tokens)


async def RetryRequest(
    request_func: Callable,
    *args,
    max_retries: int = 4,
    base_delay: float = 1.0,
    retryOn: tuple = ("429", "RESOURCE_EXHAUSTED"),
    use_jitter: bool = True,
    **kwargs
) -> Any:
    for attempt in range(max_retries):
        try:
            return await asyncio.to_thread(request_func, *args, **kwargs)

        except Exception as exc:
            errorMessage = str(exc)
            shouldRetry = any(code in errorMessage for code in retryOn)
            if not shouldRetry or attempt == max_retries - 1:
                raise
            delay = base_delay * (2**attempt)
            if use_jitter:
                delay += random.uniform(0, 0.5)
            await asyncio.sleep(delay)
