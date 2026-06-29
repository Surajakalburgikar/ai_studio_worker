import time
from worker.config import settings
from worker.jobs.fetch import JobFetcher

def start_poller() -> None:
    """Poll the backend for generation jobs in an infinite loop.
    
    Sleeps POLL_INTERVAL seconds between polls.
    Stops loop after receiving ONE job (MVP requirement).
    """
    poll_interval = settings.poll_interval
    fetcher = JobFetcher()

    while True:
        job = fetcher.fetch_job()
        if job is not None:
            print("Job Received")
            print(f"Job ID: {job.id}")
            print(f"Scene ID: {job.scene_id}")
            print(f"Shot Number: {job.shot_number}")
            print(f"Provider: {job.provider}")
            print(f"Filename: {job.filename}")
            print(f"Status: {job.status}")
            break
        else:
            print("No jobs found")
            time.sleep(poll_interval)
