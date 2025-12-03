import sys
import os
sys.path.append(os.getcwd())
import traceback

try:
    print("Attempting to import tests.test_benchmark")
    from tests import test_benchmark
    print("Import successful")
    print("Running test_benchmark_known_reconstructions")
    test_benchmark.test_benchmark_known_reconstructions()
    print("Test passed")
except Exception:
    traceback.print_exc()
