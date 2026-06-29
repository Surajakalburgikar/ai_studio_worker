from worker.models.job import GenerationJob
from worker.execution.executor import Executor
from worker.execution.result import ExecutionResult

class JobProcessor:
    """Orchestrates job execution through the executor."""
    
    def __init__(self) -> None:
        self.executor = Executor()

    def process(self, job: GenerationJob) -> ExecutionResult:
        """Processes the given job and returns the ExecutionResult.
        
        Prints:
            Job Started
            Job Finished
        """
        print("Job Started")
        result = self.executor.execute(job)
        print("Job Finished")
        return result
