from fastapi import FastAPI, HTTPException
import requests
from connect import get_weather

app = FastAPI()

#get lat long from connect.py file

@app.get("/terrain")
def get_evaluate(province:str, amphoe:str,tambon:str):
    datas = get_weather(province,amphoe,tambon)
    lat = datas["latitude"]
    lon = datas["longitude"]
    url_terrain = "https://api.open-elevation.com/api/v1/lookup"

    try:
        params = {"locations": f"{lat},{lon}"}
        response = requests.get(url_terrain, params=params)
        data = response.json()
        evaluate = data["results"][0]["elevation"]
        return {
            "province" : province,
            "amphoe" : amphoe,
            "tambon" : tambon,
            "evaluate(M)" : evaluate
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400,detail=e)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=e)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)



