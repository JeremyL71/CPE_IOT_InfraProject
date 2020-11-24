from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text
from microbit import *
import radio
from time import sleep
import sys

class Packet:
    def __init__(self, destinataire, temperature, luminosite):
        self.destinataire = destinataire
        self.temperature = temperature
        self.luminosite = luminosite
    
    def send(self):
        """
        Permet de générer le string qui va être envoyé dans le message.
        Il va contenir la termperature, la luminosité et le destinataire.
        """
        # Création du packet avec les données.
        jsonString = "{\"temperature\":%d,\"luminosite\":%d}" % (self.temperature, self.luminosite)
        # Création du packet avec la couche réseau.
        jsonString = "{\"destinataire\": \"%s\", \"packet\": %s}" % (self.destinataire, jsonString)
        return jsonString


clear_oled()

print (sys.version)

print("start main")

conf = "TL"

radio_group=51
print("radio_group: " + str(radio_group))
radio.config(group=radio_group, length=251)
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
    
    # Envoi du message:
    # ---------------------------------------#
    message = Packet("nathan aime les penis", int(temperature()), int(display.read_light_level()))
    radio.send(message.send())
    sleep(1)
    # ---------------------------------------#
    
    # Affichage sur l'écran
    # ---------------------------------------#
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
    # ---------------------------------------#
    
        
    
    

