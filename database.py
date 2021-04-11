import pymysql.cursors

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="larevel",
    charset='utf8mb4',
    autocommit=True)

#Sets the encoding to include french characters
cursor = connection.cursor()
fr = "ALTER DATABASE Larevel CHARACTER SET utf8mb4;"
cursor.execute(fr)
cursor = connection.cursor()
fr = "ALTER DATABASE Larevel COLLATE utf8mb4_0900_ai_ci;"
cursor.execute(fr)

#Remove tables to reset them
cursor = connection.cursor()
reset = "DROP TABLE IF EXISTS Panier, Inventaire, Catalogue, Boutiques, Gerants, Clients;"
cursor.execute(reset)

#Relation Clients
cursor = connection.cursor()
creation_table = "CREATE TABLE IF NOT EXISTS Clients (username varchar(100) NOT NULL, password varchar(200) NOT NULL, nom varchar(100) NOT NULL, courriel varchar(100) NOT NULL, PRIMARY KEY(username));"
cursor.execute(creation_table)
with open("MySQL/clients.txt", 'r', encoding='utf8') as item:
    liste = item.read().splitlines()
for i in range(100):
    cursor = connection.cursor()
    sql = "INSERT INTO Clients VALUE " + liste[i] + ";"
    cursor.execute(sql)

#Relation Gerants
cursor = connection.cursor()
creation_table = "CREATE TABLE IF NOT EXISTS Gerants (gid integer NOT NULL, nom varchar(100) NOT NULL, PRIMARY KEY(gid));"
cursor.execute(creation_table)
with open("MySQL/gerants.txt", 'r', encoding='utf8') as item:
    liste = item.read().splitlines()
for i in range(5):
    cursor = connection.cursor()
    sql = "INSERT INTO Gerants VALUE " + liste[i] + ";"
    cursor.execute(sql)

#Relation Boutiques
cursor = connection.cursor()
creation_table = "CREATE TABLE IF NOT EXISTS Boutiques (bid integer NOT NULL, ville varchar(100) NOT NULL, gid integer NOT NULL, PRIMARY KEY(bid), FOREIGN KEY(gid) REFERENCES Gerants (gid));"
cursor.execute(creation_table)
with open("MySQL/boutiques.txt", 'r', encoding='utf8') as item:
    liste = item.read().splitlines()
for i in range(5):
    cursor = connection.cursor()
    sql = "INSERT INTO Boutiques VALUE " + liste[i] + ";"
    cursor.execute(sql)

#Relation Catalogue
cursor = connection.cursor()
creation_table = "CREATE TABLE IF NOT EXISTS Catalogue (lid integer NOT NULL, titre varchar(100) NOT NULL, auteur varchar(100) NOT NULL, genre varchar(100) NOT NULL, annee year NOT NULL, couverture varchar(100) NOT NULL, PRIMARY KEY(lid));"
cursor.execute(creation_table)
with open("MySQL/catalogue.txt", 'r', encoding='utf8') as item:
    liste = item.read().splitlines()
for i in range(100):
    cursor = connection.cursor()
    sql = "INSERT INTO Catalogue VALUE " + liste[i] + ";"
    cursor.execute(sql)

#Relation Inventaire
cursor = connection.cursor()
creation_table = "CREATE TABLE IF NOT EXISTS Inventaire (lid integer NOT NULL, bid integer NOT NULL, quantite integer NOT NULL, type varchar(10) NOT NULL, prix double NOT NULL, FOREIGN KEY(lid) REFERENCES Catalogue (lid), FOREIGN KEY(bid) REFERENCES Boutiques (bid));"
cursor.execute(creation_table)
with open("MySQL/inventaire.txt", 'r', encoding='utf8') as item:
    liste = item.read().splitlines()
for i in range(100):
    cursor = connection.cursor()
    sql = "INSERT INTO Inventaire VALUE " + liste[i] + ";"
    cursor.execute(sql)

#Relation Panier
cursor = connection.cursor()
creation_table = "CREATE TABLE IF NOT EXISTS Panier (username varchar(100) NOT NULL, lid integer NOT NULL, bid integer NOT NULL, quantite integer NOT NULL, type varchar(10) NOT NULL, prix double NOT NULL, FOREIGN KEY(username) REFERENCES Clients (username), FOREIGN KEY(lid) REFERENCES Catalogue (lid), FOREIGN KEY(bid) REFERENCES Boutiques (bid));"
cursor.execute(creation_table)