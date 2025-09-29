import tempfile
import os
import pytest
from metric_caller import run_concurrently_from_file

def test_run_concurrently_from_file_minimal():
    # Create a temporary directory to act as the metrics directory
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a dummy Python metric file in the directory
        dummy_metric_path = os.path.join(tmpdir, "dummy_metric.py")
        with open(dummy_metric_path, "w") as f:
            f.write("def dummy_metric():\n    return 1.0\n")
        
        # Create a temporary tasks file
        tasks_file = os.path.join(tmpdir, "tasks.txt")
        with open(tasks_file, "w") as f:
            f.write("dummy_task\n")

        # Call the function with correct arguments (no 'verbosity')
        scores, times = run_concurrently_from_file(
            tasks_file=tasks_file,
            all_args={},  # or any appropriate dict expected by your code
            metrics_directory=tmpdir,
            log_file=os.path.join(tmpdir, "dummy.log")
        )

        # Basic assertions (adjust based on what your function returns)
        assert isinstance(scores, dict)
        assert isinstance(times, dict)
