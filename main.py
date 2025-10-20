from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# ✅ Allow all cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🧠 Connected WebSocket clients
clients = set()

@app.get("/")
async def home():
    return {"status": "FM WS Server running perfectly!"}


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    print(f"✅ Client connected: {ws.client}")

    try:
        while True:
            data = await ws.receive_text()
            # Broadcast message to all connected clients
            for client in list(clients):
                if client != ws:
                    try:
                        await client.send_text(data)
                    except Exception:
                        clients.remove(client)
    except WebSocketDisconnect:
        clients.remove(ws)
        print(f"❌ Client disconnected: {ws.client}")
    except Exception as e:
        print(f"⚠️ Error: {e}")
        clients.remove(ws)


if __name__ == "__main__":
    # 🔥 Fast & stable server config
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=False)
