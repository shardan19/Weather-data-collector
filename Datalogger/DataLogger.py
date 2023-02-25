import datetime
import time as tm
import requests
import json
import csv
import os.path
import schedule

def kelv_tocels(tem):
    return tem-270.15
BASE_URL="https://api.openweathermap.org/data/2.5/weather?"
print("program start")
config = open("config.json", "r")
configtoobjects = json.loads(config.read())
API_KEY=configtoobjects['ApiKey']
CITY=configtoobjects['City']

url=BASE_URL+"appid="+API_KEY+"&q="+CITY+"&lang=pl"+"&exclude=current"
 

def job():
   
    #print("time:", datetime.datetime.now())
    response=requests.get(url)
    response=response.json()
    print("recived data:",response)
    temp_kelvin=response['main']['temp']
    temp_celsius=kelv_tocels(temp_kelvin)
    maxtemp=kelv_tocels(response['main']['temp_max'])
    mintemp=kelv_tocels(response['main']['temp_min'])
    feelslike=kelv_tocels(response['main']['feels_like'])

    if os.path.exists("data.csv")==True:
        
        f =open('data.csv', 'a', newline='',encoding='utf-8')
        
        
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerow([response['weather'][0]['main'],response['weather'][0]['description'],response['weather'][0]['icon'],temp_celsius,feelslike,mintemp,maxtemp,response['main']['pressure'],response['main']['humidity'],response['sys']['sunrise'],response['sys']['sunset'],response['timezone'],response['visibility'],response['wind']['speed'],response['wind']['deg'],response['wind']['gust'],datetime.datetime.now()])
        f.close()  
    else:
       
        f =open('data.csv', 'a', newline='',encoding='utf-8')
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerow(['wheathermain','weatherdescripton','weathericon','temp','feelslike','tempmin','tempmax','pressure','humidity','sunrise','sunset','timezone','visibility','windspeed','winddeg','windgust','time'])
        
        datawriter.writerow([response['weather'][0]['main'],response['weather'][0]['description'],response['weather'][0]['icon'],temp_celsius,feelslike,mintemp,maxtemp,response['main']['pressure'],response['main']['humidity'],response['sys']['sunrise'],response['sys']['sunset'],response['timezone'],response['visibility'],response['wind']['speed'],response['wind']['deg'],response['wind']['gust'],datetime.datetime.now()])
        f.close()

schedule.every(5).seconds.do(job) 

while True:
    schedule.run_pending()
    tm.sleep(1)