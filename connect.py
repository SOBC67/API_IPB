from fastapi import FastAPI, HTTPException
import requests
from datetime import datetime,timezone
app = FastAPI()

url = "https://data.tmd.go.th/nwpapi/v1/forecast/area/place"

headers = {
    'accept': "application/json",
    'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImU5NDg1MWE2MGJkNDRhODA0NmZlY2IxNDIyZGMwMGZkMDYzZjQ1NzVjMDJkM2NmZmZlMzhmNTQyMWMzNzAwMjE5YzZjODMxZjc2NzFlYTZiIn0.eyJhdWQiOiIyIiwianRpIjoiZTk0ODUxYTYwYmQ0NGE4MDQ2ZmVjYjE0MjJkYzAwZmQwNjNmNDU3NWMwMmQzY2ZmZmUzOGY1NDIxYzM3MDAyMTljNmM4MzFmNzY3MWVhNmIiLCJpYXQiOjE3NDIxODA5OTYsIm5iZiI6MTc0MjE4MDk5NiwiZXhwIjoxNzczNzE2OTk2LCJzdWIiOiIzNzUxIiwic2NvcGVzIjpbXX0.c8zSvwzTtpKRLPjB5clbxHxcZGzK8JGKftcOEK7-5E3msx0c5FCyVtzrWdIY1n6OIuUMjHuFnBiRt2hfZ6Q-rcuJCR0hi3bsrnXY7nJdJY-aJPfS-mNe99X1ahEICKvD6m98gyoeXgbEJBn4i6P4Ttcuar9XuUWcfrJAHp75r5lbEBIELNjixDC-k0Hplp7ZGIBebk2tQKPWrjcgKsC9Rw3CPoC28w42F7ZrTu_NfAALZbbmlv4j-YfJ8K5YRsieWvoQ8I6R4WoBqBiuqu94LrOcCSQwiuo7xJyEdYZbXhC_cCk9gLHgd2MIsgysm6gys87ZZZOX7lvtdtv2It1FCWwTaWqKUWA059w7XETSBuf7lKhk_OvlbDaVp0TTeTcfhCy5avrj8qBZbfs9sVHrKI2wQDVRDDUzOZLw9Z2bD8LvRlLt7dpLEOSuPOLj_vekQS1PTMmv434VY491zwZrn4-720YdxI0bygSaC1fjSCGeAN2CIUv5x7Tk0GqoVW-RM-QqINTx6RRDQV4XKj0-CX3Fs1Ixh8oqpUwos-E0sHDaneHcKe3xDDpZ2Ce3vR5Y6RapNv5B_9NUH4bu26imsVUbSXkfIpO9U9hw96xUfMiwa1xdBhl69bQK_G_8edpI1Z-2o8OWzbAzz_yXQC6M-XhEMiL7xJ9H2CLIXa9EdsE",
    }


@app.get("/weather")
def get_weather(province: str, amphoe: str,tambon: str):
    params = {
          "domain":"2", 
          "province": province, 
          "amphoe": amphoe,
          "tambon": tambon, 
          "fields":"tc,rh,rain,slp,cond", 
          "starttime":"2025-03-20T22:00:00"
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
        raise HTTPException(status_code=500, detail=e)