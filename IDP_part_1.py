from fastapi import FastAPI, HTTPException
import requests
from datetime import datetime,timezone
app = FastAPI()

url = "https://data.tmd.go.th/nwpapi/v1/forecast/area/place"

headers = {
    'accept': "application/json",
    'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImI0MDc5MTU1NTE0ZTNlMmZlNGE1NmM0Y2Q2NGZmZTM1ODAyYjc2NDM3Yzk1OWE0ZmQ2NTViMTZmZmVhYTg4YmIyY2ViZmY3NGMyMDAzMjUwIn0.eyJhdWQiOiIyIiwianRpIjoiYjQwNzkxNTU1MTRlM2UyZmU0YTU2YzRjZDY0ZmZlMzU4MDJiNzY0MzdjOTU5YTRmZDY1NWIxNmZmZWFhODhiYjJjZWJmZjc0YzIwMDMyNTAiLCJpYXQiOjE3NDQ4NzI5NTgsIm5iZiI6MTc0NDg3Mjk1OCwiZXhwIjoxNzc2NDA4OTU4LCJzdWIiOiIzNzUxIiwic2NvcGVzIjpbXX0.UE73ZngLP6UkIS3wSbHSkGJ8zWJDzp9xIAeTinLrssGRJ9096M4nxrb0y_hj2Kpt7okow3TdcnMfu8pK88wNjRySr9YAxnUwQbjNh_o8yJn8VFYwLrr_ZsSqCJzWNgIdHEKM6jEPYGrqpa--4MFf8z3P9OzyCnnrRISP6c7VcobshaRaIj9TGtDproQ8lu7I4MKxSlgznyV4BRjiX3KRnTrXHrYVInfmBS1QZ4EUQlIpsAZgsgqckBq36fak_gg2N6CS3p2WAfcb7c3kcG5levnZ4BKMqw8uwFP-Z6lhG4CyrG33hvNbzAhedFR9E4frO8Fk26mjLRQomFLYYg3rfDi_JK0FFSS6ClChA7DiLZq4uN5I-xSWqLXvaoXhFaR6pVB6qG2Evag_mBxzY5TZsa4_dhhy5rZPDc8OI1BHtVDsh-epBN3Np5fuXsaDA4CZ8OaP5TWWYWq3IGANVoovZ9G3hSKKbYAJA4wQVEpcTTglqeh77IspY3TeCWBThR8u4XFEOKei_dVDptnPGwlPqafKXlkFK6P_0_Crzs7_DeS4BCe1SaTG-OLiPQoqEj-MaiFClRbxjFdEs_LVRO-qVElqubSFV1ql3g04QPAezyPpsiritLtnyaojAH7eT1GeKjHMOE6DYkQLtltOZDfqmoN8zbXnQyKPuI-kMsFzAdA",
    }
today = datetime.now().replace(hour=22,minute=0,second=0,microsecond=0)
starttime = today.isoformat()

@app.get("/weather")
def get_weather(province: str, amphoe: str,tambon: str):
    params = {
          "domain":"2", 
          "province": province, 
          "amphoe": amphoe,
          "tambon": tambon, 
          "fields":"tc,rh,rain,slp,cond",
          "starttime": starttime
    }

    try:
        response = requests.get(url,headers=headers,params= params)


        #convert to json
        data=response.json()
        #access weatherForecasts
        forecast = data["WeatherForecasts"]

        #base location
        location = forecast[0]["location"]
        #data
        temt = forecast[0]["forecasts"][0]

        #date
        dat_e = temt["time"]

        #lat,lon
        lat = location["lat"]
        lon = location["lon"]
        #data
        tc = temt["data"]["tc"]
        rh = temt["data"]["rh"]
        rain = temt["data"]["rain"]
        slp = temt["data"]["slp"]
        cond = temt["data"]["cond"]

        #condition of con
        condition_dict = {
            1: "clear", 2: "Partly cloudy", 3: "cloudy", 4: "Partly cloudy", 5: "Overcast",
            6: "Light rain", 7: "Heavy rain", 8: "Very cold", 9: "Cold", 10: "Cool",
            11: "Very hot"}
        condd = condition_dict.get(cond, "can't identify")

        #return data
        return {
            "date": dat_e,
            "latitude": lat,
            "longitude": lon,
            "temperature (c)" : tc,
            "humidity (%)" : rh,
            "rain (mm)" : rain,
            "slp" : slp,
            "condition" : condd
        }


    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400,detail=e)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=e)
    except Exception as e:
        raise HTTPException(status_code=500, detail="don't find data")