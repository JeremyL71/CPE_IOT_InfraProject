from microbit import *
import radio

radio.config(group=1)
radion.on()

# Emetteur
while True:
    radio.send(str(temperature()))
    sleep(10)
