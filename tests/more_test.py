import unittest
import tempfile
import os
from unittest import mock
from metric_caller import run_concurrently_from_file, import_metric_module

class TestMetricCallerFullCoverage(unittest.TestCase):
    def setUp(self):
        # Temporary directory for metrics
        self.tmpdir = tempfile.TemporaryDirectory()
        self.metrics_dir = self.tmpdir.name

        # Metric 1: normal
        self.metric1_path = os.path.join(self.metrics_dir, "metric1.py")
        with open(self.metric1_path, "w") as f:
            f.write(
                "def run_metric(task_name, all_args, log_queue):\n"
                "    return {task_name: 1}, 0.1\n"
            )

        # Metric 2: raises exception
        self.metric2_path = os.path.join(self.metrics_dir, "metric2.py")
        with open(self.metric2_path, "w") as f:
            f.write(
                "def run_metric(task_name, all_args, log_queue):\n"
                "    raise ValueError('fail')\n"
            )

        # Tasks file with multiple tasks
        self.tasks_file = os.path.join(self.tmpdir.name, "tasks.txt")
        with open(self.tasks_file, "w") as f:
            for i in range(10):  # 10 tasks
                f.write(f"task{i}\n")

        # Log file
        self.log_file = os.path.join(self.tmpdir.name, "log.txt")

    def tearDown(self):
        self.tmpdir.cleanup()

    # -------------------------
    # Tests for import_metric_module
    # -------------------------
    def test_import_metric_module_success(self):
        module = import_metric_module(self.metric1_path)
        self.assertTrue(hasattr(module, "run_metric"))

    def test_import_metric_module_failure(self):
        with self.assertRaises(Exception):
            import_metric_module("/non/existent/path.py")

    # -------------------------
    # Tests for run_concurrently_from_file
    # -------------------------
    def test_run_concurrently_basic(self):
        scores, times = run_concurrently_from_file(
            self.tasks_file, all_args={}, metrics_directory=self.metrics_dir, log_file=self.log_file
        )
        self.assertIn("task0", scores)
        self.assertEqual(scores["task0"], 1)

    def test_run_concurrently_with_exception_metric(self):
        os.remove(self.metric1_path)  # only exception metric left
        scores, times = run_concurrently_from_file(
            self.tasks_file, all_args={}, metrics_directory=self.metrics_dir, log_file=self.log_file
        )
        self.assertIn("task0", scores)

    # -------------------------
    # Mocked multiprocessing tests
    # -------------------------
    @mock.patch("metric_caller.multiprocessing.Pool")
    def test_run_concurrently_mocked_pool(self, mock_pool):
        mock_pool.return_value.__enter__.return_value.map.return_value = [
            ({"task0": 42}, 0.1)] * 10
        scores, times = run_concurrently_from_file(
            self.tasks_file, all_args={}, metrics_directory=self.metrics_dir, log_file=self.log_file
        )
        self.assertEqual(scores["task0"], 42)

    # -------------------------
    # Multiple tasks metrics coverage
    # -------------------------
    def test_run_multiple_tasks(self):
        scores, times = run_concurrently_from_file(
            self.tasks_file, all_args={}, metrics_directory=self.metrics_dir, log_file=self.log_file
        )
        self.assertEqual(len(scores), 10)

    def test_all_scores_are_numeric(self):
        scores, times = run_concurrently_from_file(
            self.tasks_file, all_args={}, metrics_directory=self.metrics_dir, log_file=self.log_file
        )
        for value in scores.values():
            self.assertIsInstance(value, int)

    def test_time_values_are_float(self):
        scores, times = run_concurrently_from_file(
            self.tasks_file, all_args={}, metrics_directory=self.metrics_dir, log_file=self.log_file
        )
        for t in times.values():
            self.assertIsInstance(t, float)

    # -------------------------
    # Edge cases
    # -------------------------
    def test_empty_
