import asyncio
import random
import time

from core.packet import Packet
from core.logger import Logger


class Client:

    def __init__(
        self,
        client_id,
        region,
        dns,
        load_balancer,
        metrics,
        tracer,
        retry_attempts=3
    ):

        self.client_id = client_id
        self.region = region

        self.dns = dns
        self.load_balancer = load_balancer

        self.retry_attempts = retry_attempts

        self.metrics = metrics
        self.tracer = tracer

    async def simulate_packet_loss(self):

        if random.random() < 0.2:

            await self.metrics.record_packet_loss()

            raise Exception(
                "Packet lost in transit"
            )

    async def send_request(
        self,
        domain,
        payload
    ):

        await self.metrics.record_request()

        trace_id = self.tracer.start_trace()

        Logger.log(
            self.client_id,
            f"[{self.region}] "
            f"Starting trace "
            f"{trace_id[:8]}"
        )

        packet = Packet(
            source=self.client_id,
            destination=domain,
            payload=payload,
            trace_id=trace_id
        )

        request_start = time.time()

        for attempt in range(
            1,
            self.retry_attempts + 1
        ):

            try:

                Logger.log(
                    self.client_id,
                    f"Attempt #{attempt}"
                )

                await asyncio.sleep(
                    random.uniform(0.1, 0.5)
                )

                await self.simulate_packet_loss()

                resolved = await self.dns.resolve(
                    domain,
                    trace_id
                )

                if not resolved:

                    await self.metrics.record_failure()

                    return

                response = (
                    await self.load_balancer.route(
                        packet,
                        self.region
                    )
                )

                latency = round(
                    time.time() -
                    request_start,
                    2
                )

                await self.metrics.record_success(
                    latency
                )

                Logger.log(
                    self.client_id,
                    f"Response from "
                    f"{response['region']} "
                    f"server"
                )

                self.tracer.print_trace(
                    trace_id
                )

                return response

            except Exception as error:

                Logger.log(
                    self.client_id,
                    f"ERROR: {error}"
                )

                Logger.log(
                    self.client_id,
                    "Retrying request..."
                )

                await asyncio.sleep(1)

        await self.metrics.record_failure()

        Logger.log(
            self.client_id,
            "Request failed after retries"
        )

        self.tracer.print_trace(
            trace_id
        )

        return None