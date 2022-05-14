from tkinter import *
import json
import requests
# VEML6070 Driver Example Code
from simpleio import map_range 
import time
import busio
import board
import adafruit_veml6070
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from numpy import interp
import Adafruit_DHT
import httplib2 as httplib
import urllib

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
import Adafruit_BMP.BMP085 as BMP085 # Imports the BMP library

sensor = BMP085.BMP085()







HEIGHT=400
WIDTH=800



def weather(temp,hum,uv,pressure,altitude,sealvl,wdir,wspeed):
    data = "Temperature : "+str(round(temp,2))+'*C\t'
    data+="Humidity : "+str(round(hum,2))+'%\n\n'
    data+="Pressure : "+str(pressure)+'Pa\n\n'
    data+="Altitude : "+str(round(altitude,2))+'m\n\n'
    data+="Sea Level : "+str(sealvl)+'Pa\n\n'
    data+="Wind Direction : "+str(wdir)+'\t'
    data+="Wind Speed : "+str(wspeed)+'m/s\n\n'

    show['text']=data



root=Tk()


root.title("weather")
root.configure(background="black")



canvas = Canvas(root,height=HEIGHT,width=WIDTH).pack()

background_img = PhotoImage(file="pic.png")
Label(root,image=background_img).place(relx=0,rely=0,relwidth=1,relheight=1)


lower_frame=Frame(root,bg="black",bd=3)
lower_frame.place(relx=0.5,rely=0.3,relwidth=0.75,relheight=0.45,anchor="n")
show=Label(lower_frame,bg="#f2f2f2",)
show.config(font=("Courier", 12))
show.place(relx=0,rely=0,relwidth=1,relheight=1)
weather(0,0,0,0,0,0,0,0)
#####################################################################


def cloud(temp,hum,risk_level,pressure,alti,sealvl,windir,windspd):
        #Calculate CPU temperature of Raspberry Pi in Degrees C
        data = {'key':"OYCKDRDTYZY4SK8K",'field1':temp,'field2':hum,'field3':risk_level,'field4':pressure,'field5':alti,'field6':sealvl,'field7':windir,'field8':windspd};print(data)
        params =urllib.parse.urlencode(data) 
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.Http()
        try:
            response = conn.request("http://api.thingspeak.com:80/update",method="POST", body=params, headers=headers)[0]
            #response = conn.getresponse()
            print(temp)
            print(response.status, response.reason)
            #data = response.read()
            conn.close()
        except:
            print("connection failed")
def getBMP():
        temp = sensor.read_temperature()
        pressure  = sensor.read_pressure()
        altitude = sensor.read_altitude()
        sealvl = sensor.read_sealevel_pressure()
        print( 'Temp = {0:0.2f} *C'.format(sensor.read_temperature())) 
        print( 'Pressure = {0:0.2f} Pa'.format(sensor.read_pressure())) 
        print( 'Altitude = {0:0.2f} m'.format(sensor.read_altitude())) 
        print('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()))
        return temp,pressure,altitude,sealvl


def adc_to_wind_speed(val):
    voltage_val = val / 65535 * 3.3
    return round(map_range(val, 0.4, 2, 0, 32.4),1)

# Create the I2C bus

def getDirection(direction): 
    if(direction < 22):
        return "N";
    elif (direction < 67):
        return "NE";
    elif (direction < 112):
        return "E";
    elif (direction < 157):
        return "SE";
    elif(direction < 212):
        return "S";
    elif (direction < 247):
        return "SW";
    elif (direction < 292):
        return "W";
    elif(direction < 337):
        return "NW";
    else:
        return "North"
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P0)
wind_chan = AnalogIn(ads, ADS.P1)

uv = adafruit_veml6070.VEML6070(i2c)

print("{:>5}\t{:>5}".format('raw', 'v'))
LastValue = 0
direction = None
def getWindDir():
    global LastValue
    global direction
    data = interp(chan.voltage,[0,4.096],[0,360])
    if(data > 360):
        data = data - 360;
    if(data < 0):
        data = data + 360;
    if(abs(data - LastValue)> 5):
        direction = getDirection(data);
        LastValue = data;
    return direction
    
def mainProgram():
    uv_raw = uv.uv_raw
    risk_level = uv.get_index(uv_raw)
    tmp , pressure,alti,sealvl = getBMP()
    wind_speed = adc_to_wind_speed(wind_chan.voltage)
    #tmp , pressure ,alti,sealvl = 0,0,0,0
    print("Reading: {0} | Risk Level: {1} | Wind Dir: {2} | Speed :{3} m/s".format(uv_raw, risk_level,"NE",wind_speed))
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}*C |  Humidity={1:0.1f}%".format(temperature, humidity))
    else:
        print("Failed to retrieve data from humidity sensor")
    cloud(temperature,humidity,uv_raw,pressure,alti,sealvl,"NE",wind_speed)
    weather(temperature,humidity,uv_raw,pressure,alti,sealvl,"NE",wind_speed)
    root.after(1000, mainProgram)   



root.after(1000, mainProgram)


root.mainloop()