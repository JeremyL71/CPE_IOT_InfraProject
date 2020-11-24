from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text
from microbit import *
import radio
from time import sleep
import sys

print (sys.version)

print("start main")
conf = "LT"

radio_group=1
print("radio_group: " + str(radio_group))
radio.config(group=radio_group)
radio.on()

initialize(pinReset=pin0)

while True:
    print("start while")
    msg = radio.receive()
    if msg is not None:
        print("msg: "+ str(msg))
        conf = msg
    
    message_to_send = str(temperature())+" "+str(display.read_light_level())
    radio.send(message_to_send)
    
    string_temp = "temp: " + str(temperature())
    string_light = "light: " + str(display.read_light_level())
    if conf == "LT":
         add_text(0, 1, string_light)
         add_text(0, 0, string_temp)
    elif conf == "TL":
         add_text(0, 0, string_light)
         add_text(0, 1, string_temp)
    print("End while")
    
        
    
    

