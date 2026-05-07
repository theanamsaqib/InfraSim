import asyncio

from backend.event_stream import (
    event_stream
)

from network.dns import DNSResolver
from network.load_balancer import LoadBalancer
from network.geo_router import GeoRouter

from infrastructure.server import Server
from clients.client import Client

from observability.metrics import MetricsCollector

from cache.dns_cache import DNSCache

from tracing.tracer import Tracer


async def simulate_traffic(clients):

    while True:

        tasks = []

        for client in clients:

            task = client.send_request(
                domain="api.infrasim.com",
                payload="GET /users"
            )

            tasks.append(task)

        await asyncio.gather(*tasks)

        await asyncio.sleep(3)


async def publish_server_state(
    servers
):

    while True:

        await event_stream.publish_server_state(
            servers
        )

        await asyncio.sleep(1)


async def start_simulation():

    metrics = MetricsCollector()

    tracer = Tracer()

    dns_cache = DNSCache(ttl=5)

    geo_router = GeoRouter()

    servers = [

        Server(
            "INDIA-SERVER-1",
            "INDIA",
            tracer
        ),

        Server(
            "INDIA-SERVER-2",
            "INDIA",
            tracer
        ),

        Server(
            "US-SERVER-1",
            "US",
            tracer
        ),

        Server(
            "US-SERVER-2",
            "US",
            tracer
        ),

        Server(
            "EU-SERVER-1",
            "EUROPE",
            tracer
        )
    ]

    dns = DNSResolver(
        cache=dns_cache,
        metrics=metrics,
        tracer=tracer
    )

    load_balancer = LoadBalancer(
        servers,
        tracer,
        geo_router
    )

    clients = [

        Client(
            "CLIENT-INDIA-1",
            "INDIA",
            dns,
            load_balancer,
            metrics,
            tracer
        ),

        Client(
            "CLIENT-INDIA-2",
            "INDIA",
            dns,
            load_balancer,
            metrics,
            tracer
        ),

        Client(
            "CLIENT-US-1",
            "US",
            dns,
            load_balancer,
            metrics,
            tracer
        ),

        Client(
            "CLIENT-EU-1",
            "EUROPE",
            dns,
            load_balancer,
            metrics,
            tracer
        )
    ]

    await asyncio.gather(

        simulate_traffic(clients),

        publish_server_state(
            servers
        )
    )