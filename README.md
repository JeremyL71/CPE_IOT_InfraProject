# CPE_IOT_InfraProject

## Présentation du projet:
Le but étant de réaliser cette architecture:
![enter image description here](https://github.com/JeremyL71/CPE_IOT_InfraProject/blob/main/Documentations/photos/intro_sujet.PNG?raw=true)

## Micro-bit sensor/actor
### Affichage de la température et de la luminosité
Le but étant de d'afficher la température ambiante ainsi que la luminosité sur l'écran d'affichage suivante deux configurations:

    température: 25°C
    luminosité: 114

ou bien

    luminosité: 114
    température: 25°C

Cette configuration dépend de l'utilisateur et est commandé depuis l'application android.
### Mise en place
Utilisation d'un breakboard afin de relier l'écran OLED et le microbit.

 -  lien vers la datasheet  du breakboard: https://resources.kitronik.co.uk/pdf/5601b_built_edge_connector_breakout_board_for_the_bbc_microbit_datasheet_v1_1.pd
 - lien vers la bibliothèque python pour l'écran ssd1306: https://github.com/CPELyon/microbit_ssd1306
 
 ### Instructions
 Le speudo code d'instruction est le suivant: 
 ![enter image description here](https://github.com/JeremyL71/CPE_IOT_InfraProject/blob/main/Documentations/photos/sc_instruc_microbit_oled.PNG?raw=true)
## Serveur

### Fonctionnalité 

- Récupération des infos de la passerelle à travers une connexion serial.
- Stockage des données récupérer à travers la connexion serial
- 2 endpoints : 
- 1 pour donner accès aux informations stocké en base à l'application Android.
- 1 pour transférer la demande de changement d'affichage du microbit.


### Librairies

- Utilisation de la librairie JSON du a l'utilisation du JSON dans le transfert des packets.

### Utilisation 

Il y a deux évènements qui déclenche une action sur le serveur : 

- L'ajout de contenu dans le flux serial.
- Une connexion au server UDP.

### L'ajout de contenu dans le flux serial

Cet évènement va déclencher différentes actions dans l'ordre :

- Lecture du flux qui doit être au format JSON. 
- Vérification que le contenu soit bien au format JSON sinon il n'est pas traité.
- Lecture des informations de temperature et de luminosité.
- Si les informations ne sont pas présente alors le flux n'est pas traité.

- Une fois les informations récupéré du packet il y a la sauvegarde en base.
- Création d'une connexion à la base SQLite.
- Ajout des informations à travers la commande : 

```sql
INSERT INTO data(temperature, luminosite) VALUES (?1, ?2);
```

- On commit la transaction puis ferme la connexion.


### Une connexion au server UDP 

Il y a deux action depuis la connexion au server UDP. Soit le contenu du flux est : `getValues()` soit c'est un format du type `LT` ou `TL`.

Dans le cas ou c'est `getValues()` : 

- Création d'une connexion à la base de données
- Récupération des dernières données avec la requête suivante : 

```sql
SELECT temperature, luminosite FROM data ORDER BY data_id DESC LIMIT 1;
```

- Envoi des données au format JSON en retour de la connexion.

Dans le cas `LT` ou `TL`

- Récupération de l'information
- Création d'un packet au format JSON
- Envoi du packet à travers la connexion serial.


### Database

Connexion à la base de donnée via le fichier :

```bash
sqlite3 database.sqlite
```

Script d'initialisation de la base de donnée :

```sql
create table data (data_id INTEGER PRIMARY KEY AUTOINCREMENT, temperature INTEGER, luminosite INTEGER);
```

Requête pour récupérer la dernière donnée ajouté en base :

```sql
SELECT temperature, luminosite FROM data ORDER BY data_id DESC LIMIT 1;
```

Requête d'insertion de donnée dans la base :

```sql
INSERT INTO data(temperature, luminosite) VALUES (?1, ?2);
```


## Android 

Différentes actions sont possibles depuis l'application Android : 

- Récupérer les dernières valeurs enregistré depuis le microbit sur le serveur.
- Changer le format de l'affichage du microbit.

### La récupération des valeurs du microbit

Pour ces deux actions il est nécessaire de passer par le serveur à travers une connexion UDP.

Au démarrage de l'application les informations sont automatiquement récupérer au près du serveur à travers ces différentes étapes : 

- Création de la connexion UDP
- Envoi dans le packet UDP la commande suivante : `getValues()`
- Récupération de la réponse du serveur.
- On décode la réponse qui est au format JSON pour récupérer les valeurs.
- Affichage du résultat.

Pour pouvoir réaliser ces différentes actions il est nécessaire d'utiliser le système AsyncTask qui permet d'effectuer un traitement asynchrone par rapport à l'application mais de ce synchroniser pour certaines actions. Ce traitement est parfait dans notre cas car il permet de faire le requête de façon asynchrone et de ne pas être bloquant pour l'application mais de ce synchroniser pour effectuer les changements de l'affichage.

### Changer le format de l'affichage du microbit

Cette action est effectué lorsque l'utilisateur click sur le bouton `Changer format`. Cela déclenche les actions suivantes : 

- Création d'une connexion UDP avec le serveur.
- Envoi de `LT` ou `TL` en fonction du choix voulu pour l'affichage.
- Fermeture de la connexion.

Dans ce cas la il n'est pas nécessaire de faire une AsyncTask car aucun retour de la requête n'est affiché ou ne doit être synchroniser avec l'application.
