import sys
import traceback
try:
    from qawm.inference import dag_builder
    from qawm.core.models import Event
    from datetime import datetime, timedelta

    print("Imports successful")

    class MockTrace:
        def __init__(self, id, timestamp):
            self.id = id
            self.timestamp = timestamp

    traces = [MockTrace(f"t{i}", datetime.now() + timedelta(days=i)) for i in range(3)]
    print("Traces created")

    dag = dag_builder.infer_causal_dag(traces)
    print("DAG created")
    
except Exception:
    traceback.print_exc()
