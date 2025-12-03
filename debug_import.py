try:
    import qawm.core.api
    print(f"Import qawm.core.api successful from {qawm.core.api.__file__}")
    print(dir(qawm.core.api))
except Exception as e:
    import traceback
    traceback.print_exc()
