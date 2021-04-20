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

#Remove procedures
cursor = connection.cursor()
reset = "DROP procedure IF EXISTS updateVentes;"
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
cursor = connection.cursor()
sql = "CREATE FULLTEXT INDEX indexClientsUsername on Clients(username);"
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
cursor = connection.cursor()
sql = "CREATE FULLTEXT INDEX indexGerantsNom on Gerants(nom);"
cursor.execute(sql)

#Relation Boutiques
cursor = connection.cursor()
creation_table = "CREATE TABLE IF NOT EXISTS Boutiques (bid integer NOT NULL, ville varchar(100) NOT NULL, gid integer NOT NULL, ventes double NOT NULL, PRIMARY KEY(bid), FOREIGN KEY(gid) REFERENCES Gerants (gid));"
cursor.execute(creation_table)
with open("MySQL/boutiques.txt", 'r', encoding='utf8') as item:
    liste = item.read().splitlines()
for i in range(5):
    cursor = connection.cursor()
    sql = "INSERT INTO Boutiques VALUE " + liste[i] + ";"
    cursor.execute(sql)
cursor = connection.cursor()
sql = "CREATE UNIQUE INDEX indexBoutiquesBid on Boutiques(bid);"
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
cursor = connection.cursor()
sql = "CREATE UNIQUE INDEX indexCatalogueLid on Catalogue(lid);"
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
cursor = connection.cursor()
sql = "CREATE INDEX indexInventaireLid on Inventaire(lid);"
cursor.execute(sql)

#Relation Panier
cursor = connection.cursor()
creation_table = "CREATE TABLE IF NOT EXISTS Panier (username varchar(100) NOT NULL, lid integer NOT NULL, bid integer NOT NULL, quantite integer NOT NULL, type varchar(10) NOT NULL, prix double NOT NULL, FOREIGN KEY(username) REFERENCES Clients (username), FOREIGN KEY(lid) REFERENCES Catalogue (lid), FOREIGN KEY(bid) REFERENCES Boutiques (bid));"
cursor.execute(creation_table)

#Routine updateVentes
cursor = connection.cursor()
sql = """
CREATE PROCEDURE updateVentes(IN user varchar(100))
BEGIN
DECLARE b integer;
DECLARE q integer;
DECLARE p double;
DECLARE lecture_complete integer DEFAULT FALSE;
DECLARE curseur CURSOR FOR SELECT P.bid, P.quantite, P.prix from Panier P where P.username=user;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET lecture_complete = TRUE;
OPEN curseur;
lecteur: LOOP
FETCH curseur INTO b, q, p;
IF lecture_complete THEN
LEAVE lecteur;
END IF;
SELECT B.ventes into @temp from Boutiques B where B.bid=b;
IF b = 1 THEN
UPDATE Boutiques B SET ventes:= @temp + q * p where B.bid=1;
ELSEIF b = 2 THEN
UPDATE Boutiques B SET ventes:= @temp + q * p where B.bid=2;
ELSEIF b = 3 THEN
UPDATE Boutiques B SET ventes:= @temp + q * p where B.bid=3;
ELSEIF b = 4 THEN
UPDATE Boutiques B SET ventes:= @temp + q * p where B.bid=4;
ELSE
UPDATE Boutiques B SET ventes:= @temp + q * p where B.bid=5;
END IF;
END LOOP lecteur;
CLOSE curseur;
END;
"""
cursor.execute(sql)