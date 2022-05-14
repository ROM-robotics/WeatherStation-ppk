import time
import board
import busio
import adafruit_veml6070

i2c = busio.I2C(board.SCL, board.SDA)

veml = adafruit_veml6070.VEML6070(i2c)

while True:
    print(veml.uv_index)
    time.sleep(1)
