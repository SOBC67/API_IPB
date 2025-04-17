from fastapi import FastAPI, HTTPException,Request
from fastapi.responses import HTMLResponse
import ee
import requests

#start earth engine
ee.Authenticate(auth_mode="paste")
ee.Initialize(project="ee-sirawichsa")

#start fastapi
app = FastAPI()


@app.get("/terrain")
async def get_terrain(lat:float,lon:float,radius:int):
       #evaluate = await get_elevation(lat,lon)
       building = await get_building(lat,lon)
       elevation = await get_elevation(lat,lon)
       landuse = await get_landuse(lat,lon,radius)
       natural = await get_natural(lat,lon,radius)
       return {
            "Latitude" : lat,
            "Lontitude" : lon,
            "ชั้นความสูง(M)": elevation,
            "สิ่งปลูกสร้าง" : building,
            "ภูมิประเทศ" : landuse,
            "พืชพรรณป่าไม้": natural
       }

async def get_elevation(lat:float,lon:float):
       url = "https://api.sphere.gistda.or.th/services/geo/elevation"
       params = {
              "lon":lon,
              "lat":lat,
              "key":"B27769EC4F2B4A4FAA76EBBD7AF131EE"
              }
       response = requests.get(url,params=params)
       data = response.json()
       elevation = data[0]["elevation"]
       return elevation
       



async def get_building(lat:float,lon:float):
       url = "https://api.sphere.gistda.or.th/services/poi/search"
       params = {
              "lon":lon,
              "lat":lat,
              "limit":10,
              "key":"B27769EC4F2B4A4FAA76EBBD7AF131EE"
              }
       response = requests.get(url,params=params)
       data = response.json()
       place = []
       for item in data.get("data",[]):
              name = item.get("name","ไม่มีชื่อ")
              id = item.get("id",[])
              lat = item.get("lat",[])
              lon = item.get("lon",[]) 
              tag = item.get("tag",[])[0]
              place.append({
                     "id":id,
                     "ชื่อ":name,
                     "lat":lat,
                     "lon":lon,
                     "ประเภท":tag})
      
       return place

async def get_landuse(lat:float,lon:float,radius:int):
       url = "http://overpass-api.de/api/interpreter"
       query = f"""
       [out:json][timeout:25];
       (
       node(around:{radius},{lat},{lon})["landuse"];
       node(around:{radius},{lat},{lon})["natural"];
       );
       out body;
       """
       response = requests.get(url,params={"data":query})
       data = response.json()
       result = []
       for element in data.get("elements",[]):
              landuse= element.get("tags",{}).get("landuse") or element.get("tags",{}).get("natural","unknow")
              result.append({
                     "id" : element["id"],
                     "lat": element["lat"],
                     "lon":element["lon"],
                     "ภูมิประเทศ":landuse
              })

       return result

async def get_natural(lat:float,lon:float,radius:int):
       url = "http://overpass-api.de/api/interpreter"
       query = f"""
       [out:json][timeout:25];
       (
       node(around:{radius},{lat},{lon})["natural"="tree"];
       node(around:{radius},{lat},{lon})["natural"="wood"];
       node(around:{radius},{lat},{lon})["landuse"="forest"];
       node(around:{radius},{lat},{lon})["landuse"="orchard"];
       node(around:{radius},{lat},{lon})["landuse"="farmland"];
       node(around:{radius},{lat},{lon})["landuse"="meadow"];
       );
       out body;
       """
       response = requests.get(url, params={"data": query})
       data = response.json()
       results = []
       for element in data.get("elements",[]):
              natural = element.get("tags",{}).get("natural") or element.get("tags",{}).get("landuse","unknow")
              results.append({
                     "id":element["id"],
                     "lat":element["lat"],
                     "lon":element["lon"],
                     "พืชพรรณ":natural
              })
       return results

#get map don't success now.
@app.get("/map")
async def get_map(lat:float,lon:float):
       url = "https://api.sphere.gistda.or.th/services/snippet/embed"
       params = {
              "lon": lon,
              "lat": lat,
              "zoom":14,
              "map": "sphere_streets",
              "key": "B27769EC4F2B4A4FAA76EBBD7AF131EE",
              "marker" : True,
              "poi":"B00486671"
       }
       response = requests.get(url,params=params)
         
       return HTMLResponse(content=response.text)