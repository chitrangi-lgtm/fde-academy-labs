class CircuitOpen(Exception):
    """Raised when the breaker is open and the call is not attempted."""


class FakeClock:
    """The drill's clock: call it for the time, advance it with .tick(seconds)."""
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now

    def tick(self, seconds):
        self.now += seconds
