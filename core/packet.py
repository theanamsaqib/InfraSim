from dataclasses import dataclass, field
import uuid
import time


@dataclass
class Packet:
    source: str
    destination: str
    payload: str
    trace_id: str

    packet_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)

    def __str__(self):

        return (
            f"Packet("
            f"id={self.packet_id[:8]}, "
            f"trace={self.trace_id[:8]}, "
            f"src={self.source}, "
            f"dest={self.destination}, "
            f"payload={self.payload}"
            f")"
        )