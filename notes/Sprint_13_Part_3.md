# Sprint 13 Part 3 - Job Polling

## Files Changed
- [worker/config.py](file:///c:/Projects/AI_STUDIO_WORKER/worker/config.py): Added `poll_interval` setting (loaded from `POLL_INTERVAL` environment variable, defaulting to `5` seconds).
- [worker/models/job.py](file:///c:/Projects/AI_STUDIO_WORKER/worker/models/job.py): Created `GenerationJob` dataclass to model generation jobs returned by backend.
- [worker/backend/client.py](file:///c:/Projects/AI_STUDIO_WORKER/worker/backend/client.py): Added `get_next_job()` method, which performs a `GET` request to `/jobs/next`.
- [worker/jobs/fetch.py](file:///c:/Projects/AI_STUDIO_WORKER/worker/jobs/fetch.py): Implemented `JobFetcher` class to retrieve and instantiate next pending job from `BackendClient`.
- [worker/queue/poller.py](file:///c:/Projects/AI_STUDIO_WORKER/worker/queue/poller.py): Created `start_poller()` to continuously poll backend for pending generation jobs, print details when found, and exit (for MVP).
- [worker/main.py](file:///c:/Projects/AI_STUDIO_WORKER/worker/main.py): Integrated `start_poller()` to execute immediately after confirming successful backend connection.

## Polling Flow
1. **Connection Verification**: Worker performs initial health check with Backend.
2. **Poller Initialization**: If connection succeeds, `start_poller()` is invoked.
3. **Fetching Loop**:
   - Poller calls `JobFetcher.fetch_job()` every `POLL_INTERVAL` seconds.
   - If no pending jobs exist, logs `No jobs found` and sleeps.
   - If a job is returned:
     - Outputs:
       - `Job Received`
       - `Job ID`
       - `Scene ID`
       - `Shot Number`
       - `Provider`
       - `Filename`
       - `Status`
     - Halts execution (exiting the loop and the process) for MVP.

## Regression
- Connection logic remains fully backwards compatible.
- Exiting early on job reception preserves the MVP goal of only demonstrating worker/queue polling capability without initiating actual heavy processing/image generation.
