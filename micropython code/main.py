from machine import Pin, SoftI2C
from time import sleep
import mhz19b
import ssd1306
import consolaB
import writer

mhz_sensor = mhz19b.MHZ19BSensor(rx_sensor=17, tx_sensor=16) # connect RX and TX of the sensor to GPIO17 and GPIO16 of the microcontroller

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
display_width = 128
display_height = 64
display = ssd1306.SSD1306_I2C(display_width, display_height, i2c)
display.contrast(100)
font_writer = writer.Writer(display, consolaB)

sleep(1)
n = 0
while True:
    try:
        co2 = mhz_sensor.measure()
        if co2 == None:
            raise Exception()
            
        display.fill(0)
        
        text1 = "{co2:d}".format(co2=co2)
        text2 = "ppm"
        text1_width = font_writer.stringlen(text1)
        text2_width = font_writer.stringlen(text2)
        space = 4 # space between text1 and text2 in pixel
        text_width = text1_width + space + text2_width
        font_writer.set_textpos(int((display_width - text_width) / 2), 20)
        font_writer.printstring(text1)
        font_writer.set_textpos(int((display_width - text_width) / 2 + text1_width + space), 20)
        font_writer.printstring(text2)
        display.show()
        sleep(3)
    except Exception as e:
        display.fill(0)
        display.text("Reading sensor",0,20)
        display.text("failed.",0,35)
        display.show()
        sleep(0.5)


