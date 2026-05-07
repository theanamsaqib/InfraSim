from core.logger import Logger


class GeoRouter:

    def __init__(self):

        self.region_priority = {
            "INDIA": [
                "INDIA",
                "EUROPE",
                "US"
            ],

            "EUROPE": [
                "EUROPE",
                "US",
                "INDIA"
            ],

            "US": [
                "US",
                "EUROPE",
                "INDIA"
            ]
        }

    def get_preferred_regions(
        self,
        client_region
    ):

        Logger.log(
            "GEO_ROUTER",
            f"Selecting regions for "
            f"{client_region}"
        )

        return self.region_priority.get(
            client_region,
            ["US"]
        )