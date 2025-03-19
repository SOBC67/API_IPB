import requests
import pandas as pd
from datetime import datetime
import time

url = "https://data.tmd.go.th/nwpapi/v1/forecast/area/place"

current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
print(current_time)

params = {"domain":"2", 
          "province":"นครปฐม", 
          "amphoe":"สามพราน", 
          "fields":"tc,rh,rain,cond", 
          "starttime":datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}

headers = {
    'accept': "application/json",
    'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImU5NDg1MWE2MGJkNDRhODA0NmZlY2IxNDIyZGMwMGZkMDYzZjQ1NzVjMDJkM2NmZmZlMzhmNTQyMWMzNzAwMjE5YzZjODMxZjc2NzFlYTZiIn0.eyJhdWQiOiIyIiwianRpIjoiZTk0ODUxYTYwYmQ0NGE4MDQ2ZmVjYjE0MjJkYzAwZmQwNjNmNDU3NWMwMmQzY2ZmZmUzOGY1NDIxYzM3MDAyMTljNmM4MzFmNzY3MWVhNmIiLCJpYXQiOjE3NDIxODA5OTYsIm5iZiI6MTc0MjE4MDk5NiwiZXhwIjoxNzczNzE2OTk2LCJzdWIiOiIzNzUxIiwic2NvcGVzIjpbXX0.c8zSvwzTtpKRLPjB5clbxHxcZGzK8JGKftcOEK7-5E3msx0c5FCyVtzrWdIY1n6OIuUMjHuFnBiRt2hfZ6Q-rcuJCR0hi3bsrnXY7nJdJY-aJPfS-mNe99X1ahEICKvD6m98gyoeXgbEJBn4i6P4Ttcuar9XuUWcfrJAHp75r5lbEBIELNjixDC-k0Hplp7ZGIBebk2tQKPWrjcgKsC9Rw3CPoC28w42F7ZrTu_NfAALZbbmlv4j-YfJ8K5YRsieWvoQ8I6R4WoBqBiuqu94LrOcCSQwiuo7xJyEdYZbXhC_cCk9gLHgd2MIsgysm6gys87ZZZOX7lvtdtv2It1FCWwTaWqKUWA059w7XETSBuf7lKhk_OvlbDaVp0TTeTcfhCy5avrj8qBZbfs9sVHrKI2wQDVRDDUzOZLw9Z2bD8LvRlLt7dpLEOSuPOLj_vekQS1PTMmv434VY491zwZrn4-720YdxI0bygSaC1fjSCGeAN2CIUv5x7Tk0GqoVW-RM-QqINTx6RRDQV4XKj0-CX3Fs1Ixh8oqpUwos-E0sHDaneHcKe3xDDpZ2Ce3vR5Y6RapNv5B_9NUH4bu26imsVUbSXkfIpO9U9hw96xUfMiwa1xdBhl69bQK_G_8edpI1Z-2o8OWzbAzz_yXQC6M-XhEMiL7xJ9H2CLIXa9EdsE",
    }


def province(prv):
    params["province"] = prv

def amphoe(amp):
    params["amphoe"] = amp



x = input("กรอก จังหวัด :")
y = input("กรอก อำเภอ :")
province(x)
amphoe(y)

response = requests.get(url, headers=headers, params=params)
try:
    #blank data
    record= []
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
    cond = temt["data"]["cond"]

    #condition
    condd = ""
    if cond == 1:
        condd = "clear"
    elif cond == 2:
        condd = "Partly cloudy"
    elif cond == 3:
        condd = "cloudy"
    elif cond == 4:
        condd = "Partly cloudy"
    elif cond == 5:
        condd = "Overcast"
    elif cond == 6:
        condd = "Light rain"
    elif cond == 7:
        condd = "Heavy rain"
    elif cond == 8:
        condd = "Very cold"
    elif cond == 9:
        condd = "Cold"
    elif cond == 10:
        condd = "Cool"
    elif cond == 11:
        condd = "Very hot"
    else:
        condd = "can't identify"




    record.append([dat_e,lat,lon,tc,rh,rain,condd])
    df = pd.DataFrame(record, columns=["Date","Latitude","Longitude","Temperature (C)","Humandity (%)","Rain (mm)","Cond"])
    try:
        file_path = "C:\\Users\\frank\\OneDrive\\Desktop\\python all project\\weather_place.csv"
        df.to_csv(file_path,index=False)
        print("Success We can contain Data")
    except:
        print("Error")

except Exception as e:
    print(e)
except requests.exceptions.RequestException as e:
    print(e)
except ValueError as e:
    print(e)