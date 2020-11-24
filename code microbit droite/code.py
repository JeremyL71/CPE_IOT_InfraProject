from ssd1306_px import set_px
from ssd1306 import draw_screen, initialize, clear_oled

from microbit import *
import radio

radio.config(group=1)
radio.on()
    
# Recepteur
while True:
    message = radio.receive()
    if button_a.was_pressed():
        display.scroll(message)