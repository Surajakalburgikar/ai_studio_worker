# Sprint 13 Part 2 - Backend Communication

## Files Changed
- `worker/backend/client.py`: Implemented `BackendClient` with a `check_connection()` method utilizing `requests` (5s timeout).
- `worker/main.py`: Updated startup sequence to check backend connectivity, logging `Backend Connected / Worker Status READY` on success, or `Backend Offline / Worker Status ERROR` and exiting with status code `1` on failure.

## Connection Flow
1. Worker starts and loads environment configurations via `worker/config.py`.
2. Resolves and initializes configured Image Provider and Storage Driver.
3. Instantiates `BackendClient` pointing to the configured `BACKEND_URL`.
4. Performs a `GET` request to the backend root URL with a 5-second timeout.
5. If the backend responds with HTTP `200 OK`, connection succeeds, reporting `Worker Status READY`.
6. If the connection times out, raises a `RequestException`, or returns non-200, the check fails, reporting `Worker Status ERROR` and terminating the process.

## Lessons Learned
- External dependencies like `requests` require proper error propagation handling (e.g., catching `requests.RequestException` to handle connection refused, timeouts, DNS failures cleanly).
- Keeping environment variable overrides simple simplifies testing offline scenarios.

## Regression
- No regressions were introduced. All module interfaces (`MockProvider`, `LocalStorage`) remain functional and unchanged.
