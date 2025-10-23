from typing import Annotated
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query, Response
from typing import Any
from random import randint
from fastapi import Request

app = FastAPI(root_path="/api/v1")


@app.get("/")
async def root():
    return {"message": "Hello world"}

data: Any = [{"campaign_id":1,
         "name":"Campaign 1",
         "due_date":datetime.now(),
         "created_at":datetime.now()},

        {"campaign_id":2,
         "name":"Campaign 2",
         "due_date":datetime.now(),
         "created_at":datetime.now()}]

@app.get("/campaigns")
async def read_campaigns():
    return {"campaigns": data}

@app.get("/campaigns/{campaign_id}")
async def read_campaign(campaign_id: int):
    for campaign in data:
        if campaign.get("campaign_id") == campaign_id:
            return {"campaign": campaign}
    raise HTTPException(status_code=404, detail="Campaign not found")

@app.post("/campaigns")
async def create_campaign(body: dict[str, Any]):
    new = {
        "campaing_id":randint(3, 1000),
         "name":body.get("name"),
         "due_date":body.get("due_date"),
         "created_at":datetime.now()
         }
    data.append(new)
    return {"campaign": new}

@app.put("/campaigns/{id}")
async def update_campaign(id: int, body: dict[str, Any]):
    for index, campaing in enumerate(data):
        if campaing.get("campaign_id") == id:

            updated: Any ={
                "campaign_id":id,
                 "name":body.get("name"),
                 "due_date":body.get("due_date"),
                 "created_at":campaing.get("created_at")
                 }
            data[index] = updated
            return {"campaign": updated}
    raise HTTPException(status_code=404, detail="Campaign not found")


@app.delete("/campaigns/{id}")
async def delete_campaign(id: int):
    for index, campaign in enumerate(data):
        if campaign.get("campaign_id") == id:
            data.pop(index)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Campaign not found")


