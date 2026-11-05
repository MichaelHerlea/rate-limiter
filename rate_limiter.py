import time
import threading

class RateLimiter:
    def __init__(self, limit: int, window_seconds: float, clock=time.monotonic):
        if limit < 0:
            raise ValueError("limit must be a non-negative integer")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be a positive number")

        self.limit = limit
        self._refill_rate = limit / window_seconds
        self._clock = clock
        self._user_buckets = {}
        self._lock = threading.Lock()

    def allow(self, key: str) -> bool:
        with self._lock:
            current_time = self._clock()

            # We create a new full bucket for the user if it doesn't exist
            if key not in self._user_buckets:
                self._user_buckets[key] = [self.limit, current_time]

            tokens, last_refill_time = self._user_buckets[key]

            # We refill the bucket based on the time passed since the last refill
            tokens = min(self.limit, tokens + (current_time - last_refill_time) * self._refill_rate)
            self._user_buckets[key][0] = tokens
            self._user_buckets[key][1] = current_time

            if tokens >= 1:
                self._user_buckets[key][0] -= 1
                return True
            return False