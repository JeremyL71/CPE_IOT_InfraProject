import os


class Packet:
    def __init__(self, destinataire, temperature, luminosite):
        self.destinataire = destinataire
        self.temperature = temperature
        self.luminosite = luminosite


"""
Permet de générer le string qui va être envoyé dans le message.
Il va contenir la termperature, la luminosité et le destinataire.
"""


def send(packet):
    # Création du packet avec les données.
    print("[+] Création du packet application")
    jsonString = '{"temperature":%d,"luminosite":%d}' % (
        packet.temperature,
        packet.luminosite,
    )
    print("[+] Encrypt data here")
    # Création du packet avec la couche réseau.
    print("[+] Création du packet réseau")
    jsonString = '{"destinataire": "%s", "packet": %s}' % (
        packet.destinataire,
        jsonString,
    )

    return jsonString


"""
Méthode qui récupère le contenu du packet et soustrais les informations
"""


def receive(packet):
    destinataire = getDestinataire(packet)
    print("[+] Destinataire %s" % destinataire)
    data = getData(packet)
    print("[+] Data : %s" % data)
    print("[+] Decrypt Data here")

    temperature = getTemperature(data)
    print("[+] Temperature : %s" % temperature)

    luminosite = getLuminosite(data)
    print("[+] Luminsoite %s" % luminosite)

    return Packet(destinataire, temperature, luminosite)


"""
Recupère le destinataire du packet
"""


def getDestinataire(packet):
    return packet.split('"')[3]


"""
Récupère les données du packet
"""


def getData(packet):
    contentSplit = packet.split("{")
    return "{" + contentSplit[2][0 : len(contentSplit[2]) - 1]


"""
Récupère la température dans les données du packet
"""


def getTemperature(data):
    return data.split(":")[1].split(",")[0]


"""
Récupère la luminosité dans les données du packet
"""


def getLuminosite(data):
    luminosite = data.split(":")[2]
    return luminosite[0 : len(luminosite) - 1]


if __name__ == "__main__":
    print("[+] Création du packet avec la temperature 12 et la luminosite 14")
    print("[+] Packet : ")
    packet = send(Packet("127.0.0.1", 12, 14))
    print("[+] " + packet)

    print(packet)

    print("[+] Récupération du packet")
    packetClass = receive(packet)
