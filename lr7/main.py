import asyncio
import httpx
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List, Dict

app = FastAPI()

class Observer:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket

class CurrencyObserver:
    def __init__(self):
        self.observers: List[Observer] = []
        self.last_rates: Dict[str, dict] = {}

    async def register(self, websocket: WebSocket):
        observer = Observer(websocket)
        self.observers.append(observer)
        await websocket.accept()

    async def unregister(self, observer: Observer):
        self.observers.remove(observer)

    async def notify(self, rates):
        for observer in self.observers:
            await observer.websocket.send_text(f"Updated rates: {rates}")

    async def fetch_rates(self):
        async with httpx.AsyncClient() as client:
            response = await client.get("https://www.cbr-xml-daily.ru/daily_json.js")
            return response.json()["Valute"]

    async def check_for_updates(self):
        while True:
            new_rates = await self.fetch_rates()
            if new_rates != self.last_rates:
                await self.notify(new_rates)
                self.last_rates = new_rates
            await asyncio.sleep(60)

currency_observer = CurrencyObserver()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(currency_observer.check_for_updates())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await currency_observer.register(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await currency_observer.unregister(currency_observer.observers[-1])

@app.get("/")
async def get():
    return HTMLResponse(content=open("cont.html").read(), status_code=200)

@app.get("/rate/{currency_code}")
async def get_currency_rate(currency_code: str):
    rates = currency_observer.last_rates
    if currency_code in rates:
        return {
            "current": rates[currency_code]["Value"],
            "previous": rates[currency_code]["Previous"],
            "name": rates[currency_code]["Name"],
            "char_code": rates[currency_code]["CharCode"]
        }
    return {"error": "Currency not found"}

