from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from backend.event_stream import (
    event_stream
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

import asyncio

from simulation import (
    start_simulation
)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():

    asyncio.create_task(
        start_simulation()
    )


@app.get("/")
async def home():

    return {
        "service": "InfraSim Backend",
        "status": "running"
    }


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket
):

    print("WebSocket connection attempt")

    await event_stream.connect(
        websocket
    )

    print("WebSocket accepted")

    try:

        while True:

            await asyncio.sleep(1)

    except WebSocketDisconnect:

        print("WebSocket disconnected")

        event_stream.disconnect(
            websocket
        )