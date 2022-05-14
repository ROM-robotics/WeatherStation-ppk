import time
from simpleio import map_range
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from numpy import interp
# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
 
# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)
#chan1 = AnalogIn(ads, ADS.P1)
 
# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)
def adc_to_wind_speed(val):
    """Returns anemometer wind speed, in m/s.
    :param int val: ADC value
    """
    voltage_val = val / 65535 * 3.3
    return round(map_range(val, 0.4, 2, 0, 32.4),1)

def getDirection(direction): 
    if(direction < 22):
        print("N");
    elif (direction < 67):
        print("NE");
    elif (direction < 112):
        print("E");
    elif (direction < 157):
        print("SE");
    elif(direction < 212):
        print("S");
    elif (direction < 247):
        print("SW");
    elif (direction < 292):
        print("W");
    elif(direction < 337):
        print("NW");
    else:
        print("North")
#print("{:>5}\t{:>5}".format('raw', 'v'))
LastValue = 0
while True:
    #print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
    #data = interp(chan.voltage,[0,4.096],[0,1024])
    print(chan.voltage)
    #wind_speed = adc_to_wind_speed(chan.voltage)
    #wind_speed = (chan.value - 125) * 0.0648
    #print(wind_speed)
    """if(data > 360):
        data = data - 360;
    if(data < 0):
        data = data + 360;
    if(abs(data - LastValue)> 5):
        getDirection(data);
        LastValue = data;"""
    time.sleep(0.5)
