import traceback
try:
    from benchmarks.qawm.reconstruction_accuracy_tests import test_benchmark_known_reconstructions
    print("Import successful")
    test_benchmark_known_reconstructions()
    print("Test passed")
except Exception:
    traceback.print_exc()
