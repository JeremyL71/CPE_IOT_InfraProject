# Program to control passerelle between Android application
# and micro-controller through USB tty
import time
import argparse
import signal
import sys
import socket
import SocketServer
import serial
import threading
import json
import sqlite3
import os

HOST           = "192.168.1.43"
UDP_PORT       = 56000
MICRO_COMMANDS = ["TL" , "LT"]
FILENAME        = "values.txt"
LAST_VALUE      = "15/21"

class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        current_thread = threading.current_thread()
        print("[+] {}: client: {}, wrote: {}".format(current_thread.name, self.client_address, data))
        if data != "":
                        if data in MICRO_COMMANDS: # Send message through UART
                                sendUARTMessage(data)
                                
                        elif data == "getValues()": # Sent last value received from micro-controller
                                socket.sendto(getLastValues(), self.client_address) 
                                      
                        else:
                                print("[-] Unknown message: ",data)

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass


# send serial message 
SERIALPORT = "/dev/tty.Bluetooth-Incoming-Port"
BAUDRATE = 115200
ser = serial.Serial()

def initUART():        
        # ser = serial.Serial(SERIALPORT, BAUDRATE)
        ser.port=SERIALPORT
        ser.baudrate=BAUDRATE
        ser.bytesize = serial.EIGHTBITS #number of bits per bytes
        ser.parity = serial.PARITY_NONE #set parity check: no parity
        ser.stopbits = serial.STOPBITS_ONE #number of stop bits
        ser.timeout = None          #block read

        # ser.timeout = 0             #non-block read
        # ser.timeout = 2              #timeout block read
        ser.xonxoff = False     #disable software flow control
        ser.rtscts = False     #disable hardware (RTS/CTS) flow control
        ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
        #ser.writeTimeout = 0     #timeout for write
        print('[+] Starting Up Serial Monitor')
        try:
                ser.open()
        except serial.SerialException:
                print("[-] Serial {} port not available".format(SERIALPORT))
                exit()



def sendUARTMessage(msg):
        dataJson = json.dumps({
                'destinataire': 'Microbit',
                'packet': {
                        'format': msg
                }
        })
        ser.write(dataJson)
        print("[+] Message <" + dataJson + "> sent to micro-controller." )

def initDatabaseConnexion():
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "database.sqlite")
        return sqlite3.connect(db_path)

def insertData(data):
        con = initDatabaseConnexion()
        # Creation du curseur
        cur = con.cursor()
        # Execution de la commande SQL
        cur.execute("INSERT INTO data(temperature, luminosite) VALUES (?1, ?2);", (data['packet']['temperature'], data['packet']['luminosite']))
        # Fermeture du curseur
        cur.close()
        con.close()

def getLastValues(): 
        con = initDatabaseConnexion()
        # Creation du curseur
        cur = con.cursor()
        # Execution de la commande SQL
        cur.execute("SELECT temperature, luminosite FROM data ORDER BY data_id DESC LIMIT 1;")

        row = cur.fetchone()

        jsonString = ""

        if row != None:
                jsonString = json.dumps({
                        'destinataire': 'Android',
                        'packet': {
                                'temperature': row[0],
                                'luminosite': row[1]
                        }
                })

        # Fermeture du curseur
        cur.close()
        con.close()

        return jsonString



# Main program logic follows:
if __name__ == '__main__':
        print('[+] Initialisation de la connexion UART')
        initUART()

        print ('[+] Press Ctrl-C to quit.')
        server = ThreadedUDPServer((HOST, UDP_PORT), ThreadedUDPRequestHandler)

        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True

        try:
                server_thread.start()
                print("[+] Server started at {} port {}".format(HOST, UDP_PORT))
                while ser.isOpen() : 
                        time.sleep(1)
                        if (ser.inWaiting() > 0):
                                data_str = ser.read(ser.inWaiting())
                                try:
                                        data = json.loads(data_str)
                                        print('[+] Temperature : ' + str(data['packet']['temperature']))
                                        print('[+] Luminosite : ' + str(data['packet']['luminosite']))   
                                        insertData(data)
                                except (ValueError):
                                        print('[-] Erreur lors du parsing json')
        except (KeyboardInterrupt, SystemExit):
                server.shutdown()
                server.server_close()
                f.close()
                ser.close()
                exit(),