import asyncio
import random
import time

from core.logger import Logger


class DNSResolver:

    def __init__(
        self,
        cache,
        metrics,
        tracer
    ):

        self.cache = cache
        self.metrics = metrics
        self.tracer = tracer

        self.records = {
            "api.infrasim.com": "load_balancer"
        }

    async def resolve(
        self,
        domain,
        trace_id
    ):

        start = time.time()

        cached_result = self.cache.get(domain)

        if cached_result:

            await self.metrics.record_cache_hit()

            duration = time.time() - start

            await self.tracer.add_span(
                trace_id,
                "DNS",
                "CACHE_HIT",
                duration
            )

            return cached_result

        await self.metrics.record_cache_miss()

        Logger.log(
            "DNS",
            f"Resolving domain {domain}"
        )

        latency = random.uniform(0.3, 0.7)

        await asyncio.sleep(latency)

        resolved_address = self.records.get(domain)

        if resolved_address:

            self.cache.set(
                domain,
                resolved_address
            )

        duration = time.time() - start

        self.tracer.add_span(
            trace_id,
            "DNS",
            "RESOLVE_DOMAIN",
            duration
        )

        Logger.log(
            "DNS",
            f"Resolved {domain} → {resolved_address}"
        )

        return resolved_address