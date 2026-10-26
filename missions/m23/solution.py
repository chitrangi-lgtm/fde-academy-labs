from provided import *  # the client's code (the checker runs provided.py first)

import time


class CircuitBreaker:
    def __init__(self, failure_threshold=3, reset_timeout=30, clock=time.monotonic):
        self.state = "closed"

    def call(self, fn):
        return fn()


clock = FakeClock()
breaker = CircuitBreaker(clock=clock)
print(breaker.call(lambda: "ok"), breaker.state)
