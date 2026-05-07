import asyncio


class EventStream:

    def __init__(self):

        self.connections = []

        self.server_state = []

        self.trace_events = []

    async def connect(self, websocket):

        await websocket.accept()

        self.connections.append(websocket)

    def disconnect(self, websocket):

        if websocket in self.connections:

            self.connections.remove(websocket)

    async def broadcast(self, data):

        disconnected = []

        for connection in self.connections:

            try:

                await connection.send_json(data)

            except Exception:

                disconnected.append(connection)

        for connection in disconnected:

            self.disconnect(connection)

    async def publish_server_state(
        self,
        servers
    ):

        server_data = []

        for server in servers:

            server_data.append({
                "server_id": server.server_id,
                "region": server.region,
                "healthy": server.is_healthy
            })

        self.server_state = server_data

        await self.broadcast({
            "type": "servers",
            "data": server_data
        })

    async def publish_trace(
        self,
        trace
    ):

        self.trace_events.append(trace)

        self.trace_events = (
            self.trace_events[-10:]
        )

        await self.broadcast({
            "type": "trace",
            "data": trace
        })


event_stream = EventStream()