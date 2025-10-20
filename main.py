from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    print("🟢 Client connected:", websocket.client)

    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast to all other clients
            for client in clients.copy():
                if client != websocket:
                    await client.send_text(data)
    except:
        pass
    finally:
        clients.remove(websocket)
        print("🔴 Client disconnected:", websocket.client)


@app.get("/")
def root():
    return {"status": "🎧 Python FM Server Running OK ✅"}
