import random
import time

from core.logger import Logger
from core.exceptions import ServerDownError


class LoadBalancer:

    def __init__(
        self,
        servers,
        tracer,
        geo_router
    ):

        self.servers = servers
        self.tracer = tracer
        self.geo_router = geo_router

    async def get_healthy_servers_by_region(
        self,
        region
    ):

        healthy_servers = []

        for server in self.servers:

            if server.region != region:
                continue

            is_healthy = await server.health_check()

            if is_healthy:
                healthy_servers.append(server)

        return healthy_servers

    async def route(
        self,
        packet,
        client_region
    ):

        start = time.time()

        preferred_regions = (
            self.geo_router.get_preferred_regions(
                client_region
            )
        )

        for region in preferred_regions:

            healthy_servers = (
                await self.get_healthy_servers_by_region(
                    region
                )
            )

            if healthy_servers:

                selected_server = random.choice(
                    healthy_servers
                )

                Logger.log(
                    "LOAD_BALANCER",
                    f"Routing packet "
                    f"{packet.packet_id[:8]} "
                    f"to {selected_server.server_id} "
                    f"({region})"
                )

                duration = time.time() - start

                await self.tracer.add_span(
                    packet.trace_id,
                    "LOAD_BALANCER",
                    f"ROUTE_TO_{region}",
                    duration
                )

                response = (
                    await selected_server.handle_request(
                        packet
                    )
                )

                return response

        Logger.log(
            "LOAD_BALANCER",
            "No healthy regional servers"
        )

        raise ServerDownError(
            "All regional servers unavailable"
        )