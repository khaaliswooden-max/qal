import sys
import os
sys.path.append(os.getcwd())
import traceback

try:
    from tests.test_benchmark import test_benchmark_known_reconstructions
    print("Import successful")
    test_benchmark_known_reconstructions()
    print("Test passed")
except Exception:
    traceback.print_exc()
