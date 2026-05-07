import time

from core.logger import Logger


class DNSCache:

    def __init__(self, ttl=5):

        self.cache = {}
        self.ttl = ttl

    def get(self, domain):

        if domain not in self.cache:

            Logger.log(
                "CACHE",
                f"CACHE MISS for {domain}"
            )

            return None

        cached_data = self.cache[domain]

        current_time = time.time()

        if current_time > cached_data["expires_at"]:

            Logger.log(
                "CACHE",
                f"CACHE EXPIRED for {domain}"
            )

            del self.cache[domain]

            return None

        Logger.log(
            "CACHE",
            f"CACHE HIT for {domain}"
        )

        return cached_data["value"]

    def set(self, domain, value):

        expires_at = time.time() + self.ttl

        self.cache[domain] = {
            "value": value,
            "expires_at": expires_at
        }

        Logger.log(
            "CACHE",
            f"Stored {domain} in cache"
        )