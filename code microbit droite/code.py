from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text
from microbit import *
import radio
from time import sleep
import sys


clear_oled()

print (sys.version)

print("start main")

conf = "TL"

radio_group=51
print("radio_group: " + str(radio_group))
radio.config(group=radio_group)
radio.on()

msg = None

initialize(pinReset=pin0)

while True:
    print("start while")
    msg = radio.receive()
    if msg is not None:
        print("msg: "+ str(msg))
        conf = msg
        clear_oled()
    
    message_to_send = str(temperature())+" "+str(display.read_light_level())
    print("Message send: " + message_to_send)
    radio.send(message_to_send)
    print("curent temp: " + str(temperature()))
    print("curent light: " + str(display.read_light_level()))
    sleep(1)
    
    string_temp = "temp: " + str(temperature())
    string_light = "light: " + str(display.read_light_level())
    print("string_temp: " + string_temp)
    print("string_light: " + string_light)
    
    print("conf: " + conf)
    if conf == "LT":
         add_text(0, 0, string_light)
         add_text(0, 1, string_temp)
    elif conf == "TL":
         add_text(0, 1, string_light)
         add_text(0, 0, string_temp)
    print("End while")
    
        
    
    

