import asyncio
import os


class Dashboard:

    def __init__(self, metrics):

        self.metrics = metrics

    async def start(self):

        while True:

            os.system("cls" if os.name == "nt" else "clear")

            data = self.metrics.get_metrics()

            print("\n========== InfraSim Dashboard ==========\n")

            print(f"Total Requests      : {data['total_requests']}")
            print(f"Successful Requests : {data['successful_requests']}")
            print(f"Failed Requests     : {data['failed_requests']}")

            print(f"\nServer Failures     : {data['server_failures']}")
            print(f"Packet Loss Events  : {data['packet_loss_events']}")

            print(f"\nCache Hits          : {data['cache_hits']}")
            print(f"Cache Misses        : {data['cache_misses']}")

            print(f"\nAverage Latency     : {data['average_latency']} sec")
            print(f"System Uptime       : {data['uptime_seconds']} sec")

            print("\n========================================\n")

            await asyncio.sleep(1)