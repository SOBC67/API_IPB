from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from connect import get_weather
from terrain_api import get_terrain


app = FastAPI()

#connect to MongoDB
mongo_url = "mongodb://localhost:27017"
client = AsyncIOMotorClient(mongo_url)
db = client.mydatabase
collection1 = db.weather_forecast
collection2 = db.terrain

class Data(BaseModel):
    date: str
    latitude: float 
    longitude: float
    temperature: float
    humidity: float
    rain: float
    slp: float
    condition: str

class Data2(BaseModel):
    latitude: float 
    longitude: float
    ชั้นความสูงM : float
    สิ่งปลูกสร้าง : str
    ภูมิประเทศ : str
    พืชพรรณป่าไม้ : str




#add data weather to mongo db
#////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.post("/weather/fetch")
async def create_item(province:str,amphoe:str,tambon:str):
    get_api = await get_weather(province,amphoe,tambon)
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
    result = await collection1.insert_one(data_dict)
    return {"id": str(result.inserted_id),
            "province":province,
            "Amphoe":amphoe,
            "Tambon":tambon,
            "message":"weather data added"}
#////////////////////////////////////////////////////////////////////////////////////////////////////


#////////////////////////////////////////////////////////////////////////////////////////////////////
#add data terrain to mongo db
@app.post("/terrain/fetch")
async def create_item_terrain(lat:float,lon:float,radius:int):
    get_api = await get_terrain(lat,lon,radius)
    data_dict = {
        "latitude": get_api["Latitude"], 
        "longitude": get_api["Lontitude"],
        "ชั้นความสูงM" : get_api["ชั้นความสูง(M)"],
        "สิ่งปลูกสร้าง" : get_api["สิ่งปลูกสร้าง"] ,
        "ภูมิประเทศ" : get_api["ภูมิประเทศ"],
        "พืชพรรณป่าไม้": get_api["พืชพรรณป่าไม้"] 
    }
    result = await collection2.insert_one(data_dict)
    return {"id": str(result.inserted_id),
            "lat":lat,
            "lon": lon,
            "message":"weather data added"}
#////////////////////////////////////////////////////////////////////////////////////////////////////



#get data
@app.get("/weather/")
async def get_item():
    datas = await collection1.find().to_list(100)
    for data in datas:
        data["_id"] = str(data["_id"])
    return datas

@app.get("/terrain/")
async def get_item():
    datas_2 = await collection2.find().to_list(100)
    for data in datas_2:
        data["_id"] = str(data["_id"])
    return datas_2