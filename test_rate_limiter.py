import threading

import pytest
from rate_limiter import RateLimiter

class FakeClock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now
    
    def advance(self, seconds):
        self.now += seconds

def test_rate_limiter_allows_requests_within_limit():
    clock = FakeClock()
    limiter = RateLimiter(limit=5, window_seconds=1, clock=clock)
    key = "user1"

    for _ in range(5):
        assert limiter.allow(key) is True

    assert limiter.allow(key) is False

def test_rate_limiter_resets_after_window():
    clock = FakeClock()
    limiter = RateLimiter(limit=5, window_seconds=1, clock=clock)
    key = "user1"

    for _ in range(5):
        assert limiter.allow(key) is True

    assert limiter.allow(key) is False

    clock.advance(1)

    for _ in range(5):
        assert limiter.allow(key) is True

    assert limiter.allow(key) is False

def test_rate_limiter_allows_requests_after_partial_refill():
    clock = FakeClock()
    limiter = RateLimiter(limit=5, window_seconds=1, clock=clock)
    key = "user1"

    for _ in range(5):
        assert limiter.allow(key) is True

    clock.advance(0.5)

    for _ in range(2):
        assert limiter.allow(key) is True 
    assert limiter.allow(key) is False

def test_rate_limiter_handles_multiple_users():
    clock = FakeClock()
    limiter = RateLimiter(limit=5, window_seconds=1, clock=clock)
    key1 = "user1"
    key2 = "user2"

    for _ in range(5):
        assert limiter.allow(key1) is True

    assert limiter.allow(key1) is False
    assert limiter.allow(key2) is True

def test_rate_limiter_denied_requests_do_not_consume_tokens():
    clock = FakeClock()
    limiter = RateLimiter(limit=5, window_seconds=1, clock=clock)
    key = "user1"

    for _ in range(5):
        assert limiter.allow(key) is True

    assert limiter.allow(key) is False

    clock.advance(0.1)
    assert limiter.allow(key) is False

    clock.advance(0.1)
    assert limiter.allow(key) is True
    assert limiter.allow(key) is False

def test_rate_limiter_thread_safety():
    clock = FakeClock()
    limiter = RateLimiter(limit=5, window_seconds=1, clock=clock)
    key = "user1"
    results = []

    def worker():
        for _ in range(5):
            results.append(limiter.allow(key))

    threads = [threading.Thread(target=worker) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    assert sum(results) == 5

def test_rate_limiter_allows_zero_limit():
    clock = FakeClock()
    limiter = RateLimiter(limit=0, window_seconds=1, clock=clock)
    key = "user1"

    assert limiter.allow(key) is False

@pytest.mark.parametrize(
    "limit, window_seconds",
    [
        (-1, 1),
        (5, 0),
        (5, -1),
        (0, 0),
    ]
)
def test_rate_limiter_rejects_invalid_parameters(limit, window_seconds):
    with pytest.raises(ValueError):
        RateLimiter(limit=limit, window_seconds=window_seconds)