import time
from worker.config import settings
from worker.jobs.fetch import JobFetcher
from worker.jobs.process import JobProcessor

def start_poller() -> None:
    """Poll the backend for generation jobs in an infinite loop.
    
    Sleeps POLL_INTERVAL seconds between polls.
    Stops loop after receiving ONE job (MVP requirement).
    """
    poll_interval = settings.poll_interval
    fetcher = JobFetcher()
    processor = JobProcessor()

    while True:
        print("Polling...")
        job = fetcher.fetch_job()
        if job is not None:
            print("Job Received")
            print(f"Job ID: {job.id}")
            print(f"Scene ID: {job.scene_id}")
            print(f"Shot Number: {job.shot_number}")
            print(f"Provider: {job.provider}")
            print(f"Filename: {job.filename}")
            print(f"Status: {job.status}")
            
            # Delegate orchestration of job execution to JobProcessor
            processor.process(job)
            break
        else:
            time.sleep(poll_interval)
