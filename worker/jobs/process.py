from worker.models.job import GenerationJob
from worker.execution.executor import Executor
from worker.execution.result import ExecutionResult
from worker.reporter.reporter import Reporter

class JobProcessor:
    """Orchestrates job execution through the executor."""
    
    def __init__(self) -> None:
        self.executor = Executor()
        self.reporter = Reporter()

    def process(self, job: GenerationJob) -> ExecutionResult:
        """Processes the given job and returns the ExecutionResult.
        
        Follows the pipeline flow:
        report_started() -> execute() -> report_progress() -> report_completed()
        On exceptions: report_failed()
        """
        try:
            self.reporter.report_started(job)
            
            result = self.executor.execute(job)
            
            if not result.success:
                raise Exception(result.message)
                
            self.reporter.report_progress(job, 50)
            self.reporter.report_completed(job, result)
            return result
        except Exception as e:
            self.reporter.report_failed(job, e)
            return ExecutionResult(
                success=False,
                provider=self.executor.image_provider.get_name(),
                generation_time=0.0,
                image_path="",
                message=str(e)
            )
