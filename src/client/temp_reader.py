from config import *
import os
import time
import board
import textwrap
import busio
import lib.oled.SSD1331 as SSD1331
import adafruit_bme280.advanced as adafruit_bme280
from PIL import Image, ImageDraw, ImageFont


class BME280Reader:
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)

        self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(self.i2c, 0x76)
        self.bme280.sea_level_pressure = 1013.25
        self.bme280.standby_period = adafruit_bme280.STANDBY_TC_500
        self.bme280.iir_filter = adafruit_bme280.IIR_FILTER_X16
        self.bme280.overscan_pressure = adafruit_bme280.OVERSCAN_X16
        self.bme280.overscan_humidity = adafruit_bme280.OVERSCAN_X1
        self.bme280.overscan_temperature = adafruit_bme280.OVERSCAN_X2
        os.system('sudo systemctl stop ip-oled.service')

    def get_temperature(self):
        return self.bme280.temperature

    def get_humidity(self):
        return self.bme280.humidity


class OLEDWeatherDisplay:
    def __init__(self):
        self.sensor = BME280Reader()
        self.display = SSD1331.SSD1331()
        self.display.Init()

        self.image = Image.new(
            "RGB", (self.display.width, self.display.height), "WHITE")
        self.draw = ImageDraw.Draw(self.image)
        self.font_small = ImageFont.truetype("./lib/oled/Font.ttf", 10)

    def display_weather_data(self):
        temp = self.sensor.get_temperature()
        hum = self.sensor.get_humidity()

        self.draw.rectangle(
            (0, 0, self.display.width, self.display.height), outline=0, fill=0)

        self.draw.text((5, 5), f'Temp: {temp} C', font=self.font_small, fill="WHITE")
        self.draw.text((5, 20), f'Humidity: {hum} %', font=self.font_small, fill="WHITE")

        self.display.ShowImage(self.image, 0, 0)


    def display_text(self, text):
        text = textwrap.fill(text, width=20)
        self.draw.rectangle(
            (0, 0, self.display.width, self.display.height), outline=0, fill=0)
        self.draw.text((5, 5), f'{text}', font=self.font_small, fill="WHITE")

        self.display.ShowImage(self.image, 0, 0)


        


