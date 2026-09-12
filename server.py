import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

BOT_TOKEN = "8963998181:AAGvGz_roIafZGMZpCMsF0wgbqYwJqDu2TE"
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InvoiceRequest(BaseModel):
    title: str
    description: str
    payload: str
    stars: int

@app.post("/create-invoice")
async def create_invoice(req: InvoiceRequest):
    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{TELEGRAM_API}/createInvoiceLink",
            json={
                "title": req.title,
                "description": req.description,
                "payload": req.payload,
                "currency": "XTR",
                "prices": [{"label": req.title, "amount": req.stars}]
            }
        )
        data = res.json()
        if not data.get("ok"):
            raise HTTPException(status_code=400, detail=data.get("description", "Failed"))
        return {"invoice_link": data["result"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
