#!/usr/bin/env python3
import os
import sys
import unittest
import coverage
from multiprocessing import Queue

def main():
    # Set environment variables
    os.environ["LOG_FILE"] = os.path.join(os.getcwd(), "log.txt")
    os.environ["LOG_LEVEL"] = "2"

    # Start coverage
    #cov = coverage.Coverage(branch=True, source='run.py')
    cov = coverage.Coverage(branch=True, omit=["/usr/lib/python3/*"])
    cov.start()

    # Discover and run tests in the "tests" directory
    loader = unittest.TestLoader()
    suite = loader.discover("tests")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Stop coverage
    cov.stop()
    cov.save()

    # Generate report
    try:
        coverage_percent = cov.report()
        print(f"\nOverall coverage: {int(coverage_percent)}%")
    except coverage.CoverageException as e:
        print("Coverage Error:", e)

    # Exit code = 0 if all tests pass, nonzero otherwise
    sys.exit(not result.wasSuccessful())

if __name__ == "__main__":
    main()
    