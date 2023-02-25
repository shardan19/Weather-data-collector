from flask import Flask, render_template, jsonify
from flask_cors import CORS
import os.path
import json
import csv
import json
import pandas as pd
from datetime import datetime,timedelta

app = Flask(__name__)

@app.route("/")
def home():
     return render_template('home.html')
    
@app.route('/data', methods=['GET'])
def data():
    if os.path.exists("data.csv")==True:
        
        data=pd.read_csv("data.csv")
        last_row=data.iloc[-1].to_json()
        last_row=json.loads(last_row)
        
        #temp
        temp=data['temp'].to_list()
        feelsliketemp=data['feelsline'].to_list()        
        fullavgtemp=round(sum(temp)/len(temp),4)
        fullavgfeeltemp=round(sum(feelsliketemp)/len(feelsliketemp),4)
        fullmaxfeeltemp=round(max(feelsliketemp),4)
        fullminfeeltemp=round(min(feelsliketemp),4)
        fullmaxtemp=round(max(temp),4)
        fulmintemp=round(min(temp),4)
        if len(temp)%2==0:
            fullmedtem=round((temp[int(len(temp)/2)]+temp[int((len(temp)/2)+1)])/2,4)           
        else:
            fullmedtem=round(temp[int((len(temp)-1)/2)],4)
        #windspeed
        wind=data['windspeed'].to_list()
        fullavgwindspeed=round(sum(wind)/len(wind),4)
        fullmaxwindspeed=round(max(wind),4)
        fulminwindspeed=round(min(wind),4)       
        if len(wind)%2==0:
            fullmedwindspeed=round((wind[int(len(wind)/2)]+temp[int((len(wind)/2)+1)])/2,4)           
        else:
            fullmedwindspeed=round(wind[int((len(wind)-1)/2)],4)
        
        #windgust
        windgust=data['windgust'].to_list()
        fullavgwindgust=round(sum(windgust)/len(windgust),4)
        fullmaxwindgust=round(max(windgust),4)
        fullminwindgust=round(min(windgust),4)     
        #humidity
        humidity=data['humidity'].to_list()
        fullavghumidity=round(sum(humidity)/len(humidity),4)
        fullmaxhumidity=round(max(humidity),4)
        fullminhumidity=round(min(humidity),4)
        #pressure
        pressure=data['pressure'].to_list()
        fullavgpressure=round(sum(pressure)/len(pressure),4)
        fullmaxpressure=round(max(pressure),4)
        fullminpressure=round(min(pressure),4)      

        lasttime=data['time'][data['time'].count()-1]
        lastdate=datetime.strptime(lasttime,'%Y-%m-%d %H:%M:%S.%f')
        startdate=lastdate-timedelta(days=6)
        print("start:",startdate)
        days7={}
        weekDays = ("Poniedziałek","Wtorek","Środa","Czwartek","Piątek","Sobota","Niedziela")
        lastweekDays=[]
        for x in(range(7)):
            
            day=startdate +timedelta(days=x)
            lastweekDays.append(weekDays[datetime.weekday(day)])
            days7.update({weekDays[datetime.weekday(day)]:{'temp':[],'windspeed':[]}})
        
        counter=0
        for date in data['time']:           
            dateobj=datetime.strptime(date,'%Y-%m-%d %H:%M:%S.%f')
            #print(datetime.weekday(dateobj),datetime.weekday(startdate))
            delta=dateobj-startdate
            deltanow=dateobj-lastdate
            #print(delta, delta.days,"deltanow",deltanow.days)
            if deltanow.days <-6:
                pass
            elif deltanow.days>=-6:
                days7[weekDays[datetime.weekday(dateobj)]]['temp'].append(data['temp'][counter])
            
            #print(date,dateobj)
            counter+1
            #date_time_obj = datetime.strptime(row['time'], '%d/%m/%y %H:%M:%S')
        avgtemp=[]
        
        for x in days7:
            pass
            
            #c=sum(days7[x]['temp'])/len(days7[x]['temp'])
            #avgtemp.append(c)
        #data['time']=pd.to_datetime(data['time'])
        #print(days7['Niedziela']['temp'])
        time=data['time'].to_list()

        data.reset_index(inplace=True)
        
        return {"temp":temp,"time":time,"wind":wind,"days7":lastweekDays,"avgtemp7":avgtemp,
        "fullavgtemp":fullavgtemp,"fullmaxtemp":fullmaxtemp,"fulmintemp":fulmintemp,"feelsliketemp":feelsliketemp,
        "fullavgfeeltemp":fullavgfeeltemp,"fullmedtem":fullmedtem,"fullavgwindspeed":fullavgwindspeed,
        "fullmaxwindspeed":fullmaxwindspeed,"fulminwindspeed":fulminwindspeed,"fullmedwindspeed":fullmedwindspeed,
        "fullmaxfeeltemp":fullmaxfeeltemp,"fullminfeeltemp":fullminfeeltemp,
        "windgust":windgust,"fullavgwindgust":fullavgwindgust,"fullmaxwindgust":fullmaxwindgust,
        "fullminwindgust":fullminwindgust,"last_row":last_row,
        "pressure":pressure,"fullavgpressure":fullavgpressure,"fullmaxpressure":fullmaxpressure,"fullminpressure":fullminpressure,
        "humidity":humidity,"fullavghumidity":fullavghumidity,"fullmaxhumidity":fullmaxhumidity,"fullminhumidity":fullminhumidity
        ,"last_row":last_row}
    else:
        return "<p>there is no data!</p>"
@app.route('/fulldata',)
def fulldata():
    if os.path.exists("data.csv")==True:
        data=pd.read_csv("data.csv")
        return render_template('fulldata.html',column_names=data.columns.values, row_data=list(data.values.tolist()),
                           link_column="Patient ID", zip=zip)
    else:
        return "<p>there is no data!</p>"
    
if __name__=="__main__":
    CORS(app)
    app.run(debug=True)
    