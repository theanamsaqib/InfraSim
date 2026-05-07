import time
import numpy as np
from backend.event_stream import event_stream


class MetricsCollector:

    def __init__(self):

        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0

        self.total_latency = 0
        self.latest_latency = 0

        self.server_failures = 0
        self.packet_loss_events = 0

        self.cache_hits = 0
        self.cache_misses = 0

        self.start_time = time.time()

        self.latency_history = []

    async def publish_metrics(self):

        await event_stream.broadcast({
            "type": "metrics",
            "data": self.get_metrics()
        })

    async def record_request(self):

        self.total_requests += 1

        await self.publish_metrics()

    async def record_success(self, latency):

        self.successful_requests += 1

        self.total_latency += latency

        self.latest_latency = latency
        self.latency_history.append(latency)

        self.latency_history = (
            self.latency_history[-200:]
        )
        await self.publish_metrics()

    async def record_failure(self):

        self.failed_requests += 1

        await self.publish_metrics()

    async def record_server_failure(self):

        self.server_failures += 1

        await self.publish_metrics()

    async def record_packet_loss(self):

        self.packet_loss_events += 1

        await self.publish_metrics()

    async def record_cache_hit(self):

        self.cache_hits += 1

        await self.publish_metrics()

    async def record_cache_miss(self):

        self.cache_misses += 1

        await self.publish_metrics()

    def get_average_latency(self):

        if self.successful_requests == 0:
            return 0

        return round(
            self.total_latency /
            self.successful_requests,
            2
        )

    def get_uptime(self):

        return round(
            time.time() -
            self.start_time,
            2
        )

    def get_metrics(self):

        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,

            "server_failures": self.server_failures,
            "packet_loss_events": self.packet_loss_events,

            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,

            "average_latency": self.get_average_latency(),

            "latest_latency": self.latest_latency,

            "p50_latency": self.get_p50_latency(),
            "p95_latency": self.get_p95_latency(),
            "p99_latency": self.get_p99_latency(),

            "uptime_seconds": self.get_uptime()
        }
    def get_p50_latency(self):

        if not self.latency_history:
            return 0

        return round(
            np.percentile(
                self.latency_history,
                50
            ),
            2
        )


    def get_p95_latency(self):

        if not self.latency_history:
            return 0

        return round(
            np.percentile(
                self.latency_history,
                95
            ),
            2
        )


    def get_p99_latency(self):

        if not self.latency_history:
            return 0

        return round(
            np.percentile(
                self.latency_history,
                99
            ),
            2
        )