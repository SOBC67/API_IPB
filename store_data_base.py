from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from connect import get_weather



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
    slp: float
    condition: str

#add data to mongo db
@app.post("/weather/fetch")
async def create_item(province:str,amphoe:str,tambon:str):
    get_api = get_weather(province,amphoe,tambon)
    data_dict = {
        "date": get_api["date"],
        "latitude": get_api["latitude"], 
        "longitude": get_api["longitude"],
        "temperature": get_api["temperature (c)"],
        "humidity": get_api["humidity (%)"],
        "rain": get_api["rain (mm)"],
        "slp": get_api["slp (hpa)"],
        "condition": get_api["condition"],
    }
    result = await collection.insert_one(data_dict)
    return {"id": str(result.inserted_id),
            "province":province,
            "Amphoe":amphoe,
            "Tambon":tambon,
            "message":"weather data added"}

@app.get("/weather/")
async def get_item():
    datas = await collection.find().to_list(100)
    for data in datas:
        data["_id"] = str(data["_id"])
    return datas