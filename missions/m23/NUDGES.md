# Nudges (open only if stuck)

1. Keep three pieces of state: the mode, the consecutive-failure count, and when the breaker opened (from the clock).

2. On each call while open: if the timeout has passed switch to half open and try once; otherwise raise CircuitOpen before calling fn.
