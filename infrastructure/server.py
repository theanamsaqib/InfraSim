import asyncio
import random
import time

from core.logger import Logger
from core.exceptions import (
    ServerDownError
)


class Server:

    def __init__(
        self,
        server_id,
        region,
        tracer
    ):

        self.server_id = server_id

        self.region = region

        self.tracer = tracer

        self.is_healthy = True

    async def recover_server(self):

        recovery_time = random.uniform(
            5,
            10
        )

        Logger.log(
            self.server_id,
            f"Recovering in "
            f"{round(recovery_time, 1)}s"
        )

        await asyncio.sleep(
            recovery_time
        )

        self.is_healthy = True

        Logger.log(
            self.server_id,
            "Server recovered"
        )

    async def health_check(self):

        return self.is_healthy

    async def handle_request(
        self,
        packet
    ):

        start = time.time()

        if not self.is_healthy:

            raise ServerDownError(
                f"{self.server_id} unavailable"
            )

        Logger.log(
            self.server_id,
            f"[{self.region}] "
            f"Received {packet}"
        )

        failure_chance = random.random()

        if failure_chance < 0.1:

            self.is_healthy = False

            Logger.log(
                self.server_id,
                "CRASHED"
            )

            asyncio.create_task(
                self.recover_server()
            )

            raise ServerDownError(
                f"{self.server_id} crashed"
            )

        regional_latency = {

            "INDIA": (0.2, 0.5),

            "US": (0.8, 1.5),

            "EUROPE": (0.5, 1.0)
        }

        min_latency, max_latency = (
            regional_latency[
                self.region
            ]
        )

        processing_time = random.uniform(
            min_latency,
            max_latency
        )

        await asyncio.sleep(
            processing_time
        )

        duration = (
            time.time() - start
        )

        await self.tracer.add_span(
            packet.trace_id,
            self.server_id,
            f"PROCESS_{self.region}",
            duration
        )

        return {

            "server": self.server_id,

            "region": self.region,

            "processing_time": round(
                processing_time,
                2
            )
        }