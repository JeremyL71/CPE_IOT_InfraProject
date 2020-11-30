from microbit import *
import radio

radio.config(group=51)
radio.on()

uart.init(baudrate=115200)

while True:
    msg = radio.receive()
    if msg != None:
        print(msg)
    if uart.any():
        msg_bytes = uart.read()
        radio.send(msg_bytes)
