# CPE_IOT_InfraProject

lien vers la datasheet: https://resources.kitronik.co.uk/pdf/5601b_built_edge_connector_breakout_board_for_the_bbc_microbit_datasheet_v1_1.pdf


## Serveur

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