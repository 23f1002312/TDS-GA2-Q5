from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from collections import defaultdict

EMAIL = "23f1002312@ds.study.iitm.ac.in"
API_KEY = "ak_mckuhjpdbgyw2u8d068f5ym1"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Accepts requests from the grader
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class AnalyticsRequest(BaseModel):
    events: list[Event]


@app.post("/analytics")
async def analytics(
    data: AnalyticsRequest,
    x_api_key: str | None = Header(default=None)
):
    # Authentication
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    total_events = len(data.events)
    unique_users = len({e.user for e in data.events})

    revenue = 0.0
    totals = defaultdict(float)

    for e in data.events:
        if e.amount > 0:
            revenue += e.amount
            totals[e.user] += e.amount

    top_user = max(totals, key=totals.get) if totals else ""

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user,
    }


@app.get("/")
async def home():
    return {"status": "running"}
