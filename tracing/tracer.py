import time
import uuid

from core.logger import Logger

from backend.event_stream import (
    event_stream
)


class Tracer:

    def __init__(self):

        self.traces = {}

    def start_trace(self):

        trace_id = str(uuid.uuid4())

        self.traces[trace_id] = []

        return trace_id

    async def add_span(
        self,
        trace_id,
        service,
        operation,
        duration
    ):

        span = {
            "trace_id": trace_id[:8],
            "service": service,
            "operation": operation,
            "duration_ms": round(
                duration * 1000,
                2
            ),
            "timestamp": time.time()
        }

        self.traces[trace_id].append(span)

        Logger.log(
            "TRACE",
            f"[{trace_id[:8]}] "
            f"{service} → {operation} "
            f"({span['duration_ms']} ms)"
        )

        await event_stream.publish_trace(
            span
        )

    def print_trace(
        self,
        trace_id
    ):

        print(
            "\n========== DISTRIBUTED TRACE ==========\n"
        )

        print(f"Trace ID: {trace_id}\n")

        spans = self.traces.get(
            trace_id,
            []
        )

        total_duration = 0

        for span in spans:

            total_duration += (
                span["duration_ms"]
            )

            print(
                f"{span['service']} "
                f"→ {span['operation']} "
                f"→ {span['duration_ms']} ms"
            )

        print(
            f"\nTotal Trace Duration: "
            f"{round(total_duration, 2)} ms"
        )

        print(
            "\n=======================================\n"
        )