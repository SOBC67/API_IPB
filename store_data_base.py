from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

app = FastAPI()

#connect to MongoDB
mongo_url = "mongodb://localhost:27017"
client = AsyncIOMotorClient(mongo_url)
db = client.mydatabase
collection = db.weather_forecast


class Data(BaseModel):
    date: str
    latitude: float 
    longitude: float
    temperature: float
    humidity: float
    rain: float
    condition: str

#add data to mongo db
@app.post("/weather/")
async def create_item(data: Data):
    data_dict = data.dict()
    result = await collection.insert_one(data_dict)
    return {"id": str(result.inserted_id),"message":"Item added"}

@app.get("/weather/")
async def get_item():
    datas = await collection.find().to_list(100)
    for data in datas:
        data["_id"] = str(data["_id"])
    return datas